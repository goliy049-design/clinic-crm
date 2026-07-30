from django.contrib import admin

from core.admin import TenantScopedAdmin

from .models import (
    Service,
    ServiceCategory,
    ServiceVariant,
    Equipment,
    Room,
)


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(TenantScopedAdmin):
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
        "category",
        "duration_minutes",
        "price",
        "clinic",
        "is_active",
    )

    list_filter = (
        "category",
        "clinic",
        "is_active",
    )

    search_fields = (
        "name",
        "category__name",
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
        "service",
        "is_active",
    )

    search_fields = (
        "name",
        "service__name",
    )

@admin.register(Room)
class RoomAdmin(TenantScopedAdmin):
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