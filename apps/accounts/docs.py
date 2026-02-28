from drf_spectacular.utils import OpenApiResponse, inline_serializer
from rest_framework import serializers

from .serializers import OTPRequestSerializer, OTPVerifySerializer

GET_OTP = {
    "methods": ["POST"],
    "request": OTPRequestSerializer,
    "responses": {
        202: OpenApiResponse(
            response=inline_serializer(
                name="OTPRequestAcceptedResponse",
                fields={
                    "message": serializers.CharField(default="Accepted. Check your email."),
                    "status_code": serializers.IntegerField(default=202),
                },
            ),
            description="Accepted",
        ),
        429: OpenApiResponse(
            response=inline_serializer(
                name="OTPRequestThrottledResponse",
                fields={
                    "message": serializers.CharField(default="Too many requests"),
                    "status_code": serializers.IntegerField(default=429),
                },
            ),
            description="Too many requests",
        ),
    },
}


VERIFY_OTP = {
    "methods": ["POST"],
    "request": OTPVerifySerializer,
    "responses": {
        200: OpenApiResponse(
            response=inline_serializer(
                name="OTPVerifySuccessResponse",
                fields={
                    "detail": serializers.CharField(default="OTP verified successfully"),
                    "tokens": serializers.JSONField(),
                },
            ),
            description="OTP verified successfully",
        ),
        423: OpenApiResponse(
            response=inline_serializer(
                name="OTPVerifyLockedResponse",
                fields={
                    "detail": serializers.CharField(default="Locked: too many failed OTP attempts. Try again later."),
                    "unlock_eta": serializers.IntegerField(default=0),
                },
            ),
            description="Too many failed OTP attempts",
        ),
        400: OpenApiResponse(
            response=inline_serializer(
                name="OTPVerifyInvalidResponse",
                fields={
                    "detail": serializers.CharField(default="Invalid or expired OTP."),
                },
            ),
            description="Invalid or expired OTP",
        ),
    },
}