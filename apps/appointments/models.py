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
        "services.ServiceVariant",
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

        # Check appointment time validity
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                errors["end_time"] = (
                    "End time must be after start time."
                )

        # Check tenant consistency
        for field_name in (
            "patient",
            "staff",
            "service",
        ):
            related = getattr(self, field_name, None)

            if related is not None:
                if related.clinic_id != self.clinic_id:
                    errors[field_name] = (
                        "Must belong to the same clinic as the appointment."
                    )

        # Check staff working schedule
        if self.staff and self.start_time and self.end_time:

            from apps.staff.models import StaffSchedule

            appointment_date = self.start_time.date()

            appointment_start = self.start_time.time()
            appointment_end = self.end_time.time()

            has_shift = StaffSchedule.objects.filter(
                staff=self.staff,
                date=appointment_date,
                is_available=True,
                start_time__lte=appointment_start,
                end_time__gte=appointment_end,
            ).exists()

            if not has_shift:
                errors["start_time"] = (
                    "Staff member is not available during this time."
                )

        # Check overlapping appointments for same staff
        if self.staff and self.start_time and self.end_time:

            overlapping = Appointment.objects.filter(
                staff=self.staff,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time,
            )

            if self.pk:
                overlapping = overlapping.exclude(
                    pk=self.pk
                )

            if overlapping.exists():
                errors["start_time"] = (
                    "Staff member already has another appointment during this time."
                )

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        staff_name = self.staff if self.staff else "Unassigned"

        return (
            f"{self.patient} with {staff_name} "
            f"@ {self.start_time:%Y-%m-%d %H:%M}"
        )