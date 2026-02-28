from drf_spectacular.utils import OpenApiResponse, inline_serializer
from rest_framework import serializers

LIST_LOGS = {
    "methods": ["GET"],
    "responses": {
        200: OpenApiResponse(
            response=inline_serializer(
                name="AuditLogListSuccess",
                fields={
                    "message": serializers.JSONField(
                        default={
                        "numberOfPages": 1,
                        "count": 1,
                        "next": "null",
                        "previous": "null",
                        "results": [
                            {
                            "id": 1,
                            "event": "OTP_REQUESTED",
                            "email": "abc@xyz.com",
                            "ipAddress": "127.0.0.1",
                            "userAgent": "agent1",
                            "metadata": {
                                "email": "abc@xyz.com"
                            },
                            "createdAt": "2026-02-28T19:08:27.039718Z"
                            }
                        ]
                        }
                    ),
                    "status_code": serializers.IntegerField(default=200),
                },
            ),
            description="Accepted",
        ),
        403: OpenApiResponse(
            response=inline_serializer(
                name="UnauthenticatedRequestResponse",
                fields={
                    "message": serializers.CharField(default="Authentication credentials were not provided."),
                    "status_code": serializers.IntegerField(default=403),
                },
            ),
            description="Unauthenticated request",
        ),
    },
}