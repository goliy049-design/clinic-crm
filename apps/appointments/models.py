from django.core.exceptions import ValidationError
from django.db import models

from core.models import TenantModel


class AppointmentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"
    NO_SHOW = "no_show", "No Show"

class AppointmentSource(models.TextChoices):
    ADMIN_PANEL = "admin_panel", "Admin Panel"
    TELEGRAM = "telegram", "Telegram"
    WEBSITE = "website", "Website"

class Appointment(TenantModel):
    """
    Appointment record for a clinic.

    clinic comes from TenantModel.
    Patient, staff, and service are clinic-scoped models.
    Staff assignment is optional because a reservation can be created
    before the operator is selected.
    """

    patient = models.ForeignKey(
        "patients.PatientProfile",
        on_delete=models.PROTECT,
        related_name="appointments",
    )

    staff = models.ForeignKey(
        "staff.StaffProfile",
        on_delete=models.PROTECT,
        related_name="appointments",
        null=True,
        blank=True,
    )

    service = models.ForeignKey(
        "services.Service",
        on_delete=models.PROTECT,
        related_name="appointments",
    )

    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.PENDING,
    )

    source = models.CharField(
    max_length=20,
    choices=AppointmentSource.choices,
    default=AppointmentSource.ADMIN_PANEL,
    )
    
    notes = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["start_time"]
        indexes = [
            models.Index(fields=["clinic", "start_time"]),
            models.Index(fields=["staff", "start_time"]),
        ]

    def clean(self):
        super().clean()

        errors = {}

        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                errors["end_time"] = "End time must be after start time."

        for field_name in ("patient", "staff", "service"):
            related = getattr(self, field_name, None)

            if related is not None:
                if related.clinic_id != self.clinic_id:
                    errors[field_name] = (
                        "Must belong to the same clinic as the appointment."
                    )

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        staff_name = self.staff if self.staff else "Unassigned"
        return f"{self.patient} with {staff_name} @ {self.start_time:%Y-%m-%d %H:%M}"