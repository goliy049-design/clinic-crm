from django.contrib import admin

from core.admin import TenantScopedAdmin

from .models import PatientProfile


@admin.register(PatientProfile)
class PatientProfileAdmin(TenantScopedAdmin):
    list_display = ("first_name", "last_name", "clinic", "phone_number")
    list_filter = ("clinic",)
    search_fields = ("first_name", "last_name", "phone_number", "user__email")
