from django.contrib import admin

from .models import Clinic


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    # Deliberately a plain ModelAdmin, not TenantScopedAdmin: Clinic is
    # the tenant itself, so scoping it "by clinic" makes no sense. Every
    # admin user that can reach this should be platform staff.
    list_display = ("name", "slug", "is_active", "created_at")
    search_fields = ("name", "slug")
