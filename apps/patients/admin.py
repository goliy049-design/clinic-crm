from django.contrib import admin

from .models import PatientProfile


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "phone_number",
        "clinic",
    )

    search_fields = (
        "first_name",
        "last_name",
        "phone_number",
        "national_code",
    )

    list_filter = (
        "clinic",
        "gender",
    )