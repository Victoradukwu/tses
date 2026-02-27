from django.urls import path

from . import views

urlpatterns = [
    path("accounts/test-add/", views.test_add, name="test_add")]