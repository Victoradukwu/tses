from django.contrib import admin

from .models import Audit

@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ['event', 'email', 'ip_address', 'user_agent', 'metadata', 'created_at']
    history_list_display = ['event', 'email', 'ip_address', 'user_agent', 'metadata', 'created_at']
    search_fields = ['event', 'email']
    list_filter = ['event']

