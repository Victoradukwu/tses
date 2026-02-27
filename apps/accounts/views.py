from djangorestframework_camel_case.parser import CamelCaseJSONParser
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response

from tasks import Audit, create_audit_log

from .serializers import OTPRequestSerializer, OTPVerifySerializer
from .utils import User, generate_otp, get_request_data, get_tokens_for_user, validate_otp


@extend_schema(methods=["POST"], request=OTPRequestSerializer)
@api_view(["POST"])
@parser_classes([CamelCaseJSONParser])
def get_otp(request):

    serializer = OTPRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email: str = serializer.validated_data.get("email")  # type: ignore
    _ = generate_otp(email, request)
    return Response({"detail": "Please check your email"}, status=status.HTTP_202_ACCEPTED)


@extend_schema(methods=["POST"], request=OTPVerifySerializer)
@api_view(["POST"])
@parser_classes([CamelCaseJSONParser])
def verify_otp(request):

    serializer = OTPVerifySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email: str = serializer.validated_data.get("email")  # type: ignore
    otp: str = serializer.validated_data.get("otp")  # type: ignore

    data_ = get_request_data(request)

    validation_result = validate_otp(otp=otp, email=email)

    if validation_result.get("is_locked"):
        create_audit_log.delay(  # type: ignore
            Audit.OTP_LOCKED, email, data_.get("ip_address"), data_.get("user_agent"), data_.get("metadata")
        )  # type: ignore
        return Response(
            {
                "detail": "Too many failed OTP attempts. Try again later.",
                "unlock_eta": validation_result.get("unlock_eta", 0),
            },
            status=status.HTTP_423_LOCKED,
        )

    if not validation_result.get("is_valid"):
        create_audit_log.delay(  # type: ignore
            Audit.OTP_FAILED, email, data_.get("ip_address"), data_.get("user_agent"), data_.get("metadata")
        )  # type: ignore
        return Response(
            {"detail": "Invalid or expired OTP."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    user, _ = User.objects.update_or_create(email=email, defaults={})
    create_audit_log.delay(  # type: ignore
        Audit.OTP_VERIFIED, email, data_.get("ip_address"), data_.get("user_agent"), data_.get("metadata")
    )
    tokens: dict = get_tokens_for_user(user)
    return Response({"detail": "OTP verified successfully", "tokens": tokens}, status=status.HTTP_200_OK)