from djangorestframework_camel_case.parser import CamelCaseJSONParser
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.accounts.utils import generate_otp
from tasks import add_numbers

from .serializers import OTPRequestSerializer, OTPVerifySerializer


@api_view()
@permission_classes([AllowAny])
def test_add(request):
    task = add_numbers.delay(2, 3) # type: ignore

    return Response({
        "message": "Task queued",
        "task_id": task.id,
    })


@extend_schema(methods=["POST"], request=OTPRequestSerializer)
@api_view(["POST"])
@parser_classes([CamelCaseJSONParser])
def get_otp(request):

    serializer = OTPRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email: str = serializer.validated_data.get("email")  # type: ignore
    _ = generate_otp(email, request)
    return Response({"detail": "Please check your email"}, status=status.HTTP_202_ACCEPTED)

