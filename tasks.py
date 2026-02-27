from django.conf import settings
from django.core.mail import send_mail

from apps.audit.models import Audit
from celery_app import app as celery_app


@celery_app.task(name="tasks.send_otp")
def send_otp(email: str, otp: str, ttl_minutes: int):
    subject = "Your OTP Code"
    message = f"Your one-time password is {otp}. It will expire in {ttl_minutes} minutes."

    return send_mail(
        subject=subject,
        message=message,
        from_email=settings.FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


@celery_app.task(name="tasks.create_audit_log")
def create_audit_log(event: str, email: str, ip_address: str, user_agent: str, metadata: dict):
    dt = {"event": event, "ip_address": ip_address, "user_agent": user_agent, "metadata": metadata}
    Audit.objects.create(**dt)