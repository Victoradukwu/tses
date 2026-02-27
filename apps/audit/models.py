from django.db import models


class Audit(models.Model):
    OTP_REQUESTED = "OTP_REQUESTED"
    OTP_VERIFIED = "OTP_VERIFIED"
    OTP_FAILED = "OTP_FAILED"
    OTP_LOCKED = "OTP_LOCKED"
    EVENT_CHOICES = [(OTP_REQUESTED, OTP_REQUESTED), (OTP_VERIFIED, OTP_VERIFIED), (OTP_FAILED, OTP_FAILED), (OTP_LOCKED, OTP_LOCKED)]

    event = models.CharField(max_length=20, choices=EVENT_CHOICES, default=OTP_REQUESTED)
    email = models.EmailField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    metadata = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
