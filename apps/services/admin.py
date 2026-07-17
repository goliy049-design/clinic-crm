from django.contrib import admin

from core.admin import TenantScopedAdmin

from .models import Service


@admin.register(Service)
class ServiceAdmin(TenantScopedAdmin):
    list_display = ("name", "clinic", "duration_minutes", "price", "is_active")
    list_filter = ("clinic", "is_active")
    search_fields = ("name",)
