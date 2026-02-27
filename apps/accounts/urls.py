from django.urls import path

from . import views

urlpatterns = [
    path("accounts/auth/otp/request/", views.get_otp, name="get_otp"),
    path("accounts/auth/otp/verify/", views.verify_otp, name="verify_otp"),
]