from django.contrib import admin

from core.admin import TenantScopedAdmin

from .models import StaffProfile


@admin.register(StaffProfile)
class StaffProfileAdmin(TenantScopedAdmin):
    list_display = ("user", "role", "clinic", "is_active")
    list_filter = ("role", "clinic", "is_active")
    search_fields = ("user__username", "user__email")
