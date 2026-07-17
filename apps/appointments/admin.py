from django.contrib import admin

from core.admin import TenantScopedAdmin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(TenantScopedAdmin):
    # patient/staff/service dropdowns are already restricted to the
    # current clinic with no extra code here: PatientProfile, StaffProfile,
    # and Service are all TenantModel subclasses, so their default manager
    # (`objects`, a TenantManager) is already clinic-scoped by the same
    # contextvar TenantMiddleware sets for this request. Superusers see
    # every clinic's records in the dropdowns, same as everywhere else.
    list_display = ("patient", "staff", "service", "start_time", "end_time", "status", "clinic")
    list_filter = ("clinic", "status", "staff")
    search_fields = ("patient__first_name", "patient__last_name")
    date_hierarchy = "start_time"
