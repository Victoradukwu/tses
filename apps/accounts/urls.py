from django.urls import path

from . import views

urlpatterns = [
    path("accounts/test-add/", views.test_add, name="test_add"),
    path("accounts/auth/otp/request/", views.get_otp, name="get_otp"),
    # path("accounts/auth/otp/verify/", views.verify_otp, name="verify_otp"),
]