from rest_framework import serializers


class OTPRequestSerializer(serializers.Serializer):
    email: str = serializers.EmailField() # type: ignore
    

class OTPVerifySerializer(serializers.Serializer):
    email: str = serializers.EmailField() # type: ignore
    otp: str|serializers.CharField = serializers.CharField()