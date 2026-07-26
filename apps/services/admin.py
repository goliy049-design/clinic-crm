from django.contrib import admin

from core.admin import TenantScopedAdmin

from .models import (
    Service,
    ServiceLine,
    ServiceVariant,
    Equipment,
)


@admin.register(ServiceLine)
class ServiceLineAdmin(TenantScopedAdmin):
    list_display = (
        "name",
        "clinic",
        "is_active",
    )

    list_filter = (
        "clinic",
        "is_active",
    )

    search_fields = (
        "name",
    )


@admin.register(Service)
class ServiceAdmin(TenantScopedAdmin):
    list_display = (
        "name",
        "clinic",
        "is_active",
    )

    list_filter = (
        "clinic",
        "is_active",
    )

    search_fields = (
        "name",
    )


@admin.register(ServiceVariant)
class ServiceVariantAdmin(TenantScopedAdmin):
    list_display = (
        "name",
        "service",
        "duration_minutes",
        "price",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "service__name",
    )


@admin.register(Equipment)
class EquipmentAdmin(TenantScopedAdmin):
    list_display = (
        "name",
        "brand",
        "model",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "brand",
        "model",
    )