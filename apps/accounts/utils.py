import secrets
from typing import Any, cast

import redis
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.exceptions import Throttled
from rest_framework.request import HttpRequest
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from tasks import Audit, create_audit_log
from tasks import send_otp as send_otp_task

OTP_TTL_SECONDS = 5 * 60
EMAIL_RATE_LIMIT_WINDOW_SECONDS = 10 * 60
IP_RATE_LIMIT_WINDOW_SECONDS = 60 * 60
MAX_OTP_REQUESTS_PER_EMAIL = 3
MAX_OTP_REQUESTS_PER_IP = 10


def get_request_data(request: HttpRequest) -> dict[str, Any]:
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded_for:
        ip_address = forwarded_for.split(",")[0].strip()
    else:
        ip_address = request.META.get("REMOTE_ADDR", "")

    user_agent = request.META.get("HTTP_USER_AGENT", "")
    payload = getattr(request, "data", None)

    if payload is None:
        payload = request.POST.dict() if request.POST else {}

    return {
        "ip_address": ip_address,
        "user_agent": user_agent,
        "metadata": payload,
    }


def _redis_client() -> redis.Redis:
    """Get the Redis client, using the url"""
    redis_url = getattr(settings, "REDIS_URL", None) or settings.CELERY_BROKER_URL
    return redis.Redis.from_url(redis_url, decode_responses=True)


def _increment_with_ttl(client: redis.Redis, key: str, ttl_seconds: int) -> tuple[int, int]:
    count = cast(int, client.incr(key))
    ttl_remaining = cast(int, client.ttl(key))

    if ttl_remaining in (-1, -2):
        client.expire(key, ttl_seconds)
        ttl_remaining = ttl_seconds

    return count, ttl_remaining


def _enforce_rate_limit(client: redis.Redis, key: str, limit: int, ttl_seconds: int, scope: str) -> None:
    count, ttl_remaining = _increment_with_ttl(client=client, key=key, ttl_seconds=ttl_seconds)

    if count > limit:
        raise Throttled(
            detail=f"Too many OTP requests for this {scope}. Try again later.",
            wait=max(ttl_remaining, 0),
        )


def get_tokens_for_user(user:User)->dict[str, str]:
    if not user.is_active:
        raise AuthenticationFailed("User is not active")

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def generate_otp(email: str, request: HttpRequest) -> dict[str, str | int]:
    """Generate a six-digit OTP, store it in Redis, and enforce rate limits.

    Args:
        email (str): The user's email
        ip_address (str | None): The caller's IP address

    Returns:
        dict[str, str | int]: OTP metadata
    """
    request_data = get_request_data(request)
    ip_address = request_data.get('ip_address')
    normalized_email = email.strip().lower()
    normalized_ip = (ip_address or "unknown").strip().lower()
    client = _redis_client()

    email_rate_limit_key = f"otp:rate:email:{normalized_email}"
    ip_rate_limit_key = f"otp:rate:ip:{normalized_ip}"

    _enforce_rate_limit(
        client=client,
        key=email_rate_limit_key,
        limit=MAX_OTP_REQUESTS_PER_EMAIL,
        ttl_seconds=EMAIL_RATE_LIMIT_WINDOW_SECONDS,
        scope="email",
    )
    _enforce_rate_limit(
        client=client,
        key=ip_rate_limit_key,
        limit=MAX_OTP_REQUESTS_PER_IP,
        ttl_seconds=IP_RATE_LIMIT_WINDOW_SECONDS,
        scope="IP",
    )

    otp = f"{secrets.randbelow(1_000_000):06d}"
    otp_key = f"otp:code:{normalized_email}"
    client.set(name=otp_key, value=otp, ex=OTP_TTL_SECONDS)

    send_otp_task.delay(normalized_email, otp, OTP_TTL_SECONDS // 60) # type: ignore
    create_audit_log.delay(Audit.OTP_REQUESTED, normalized_email, ip_address, request_data.get('user_agent'), request_data.get('metadata'), request_data.get('created_at')) # type: ignore
    return {
        "email": normalized_email,
        "otp": otp,
        "expires_in": OTP_TTL_SECONDS,
    }
