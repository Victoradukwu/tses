from django.urls import path

from . import views

urlpatterns = [
    path("accounts/audit/logs/", views.AuditListView.as_view(), name="fetch_logs")
]