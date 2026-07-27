from django.contrib import admin

from core.admin import TenantScopedAdmin

from .models import StaffProfile, StaffService, StaffSchedule


@admin.register(StaffProfile)
class StaffProfileAdmin(TenantScopedAdmin):
    list_display = (
        "user",
        "role",
        "clinic",
        "is_active",
    )

    list_filter = (
        "role",
        "clinic",
        "is_active",
    )

    search_fields = (
        "user__username",
        "user__email",
    )


@admin.register(StaffService)
class StaffServiceAdmin(TenantScopedAdmin):
    list_display = (
        "staff",
        "service",
        "duration_minutes",
        "price",
        "is_active",
    )

    list_filter = (
        "is_active",
        "staff",
    )

    search_fields = (
        "staff__user__username",
        "service__name",
    )


@admin.register(StaffSchedule)
class StaffScheduleAdmin(TenantScopedAdmin):
    list_display = (
        "staff",
        "date",
        "start_time",
        "end_time",
        "is_available",
    )

    list_filter = (
        "date",
        "staff",
        "is_available",
    )

    search_fields = (
        "staff__user__username",
    )