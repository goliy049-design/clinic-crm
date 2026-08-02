from django.core.exceptions import ValidationError
from django.db import models

from core.models import TenantModel
from .services.availability import AvailabilityService


class AppointmentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    CHECKED_IN = "checked_in", "Checked In"
    IN_PROGRESS = "in_progress", "In Progress"
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

    # Allowed workflow transitions
    ALLOWED_STATUS_TRANSITIONS = {
        AppointmentStatus.PENDING: {
            AppointmentStatus.CONFIRMED,
            AppointmentStatus.CANCELLED,
        },
        AppointmentStatus.CONFIRMED: {
            AppointmentStatus.CHECKED_IN,
            AppointmentStatus.NO_SHOW,
            AppointmentStatus.CANCELLED,
        },
        AppointmentStatus.CHECKED_IN: {
            AppointmentStatus.IN_PROGRESS,
            AppointmentStatus.CANCELLED,
        },
        AppointmentStatus.IN_PROGRESS: {
            AppointmentStatus.COMPLETED,
        },
        AppointmentStatus.COMPLETED: set(),
        AppointmentStatus.CANCELLED: set(),
        AppointmentStatus.NO_SHOW: set(),
    }

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

        if self.staff and self.start_time and self.end_time:
            try:
                AvailabilityService(self).validate_staff_schedule()
            except ValidationError as exc:
                errors.update(exc.message_dict)

        if self.staff and self.start_time and self.end_time:
            try:
                AvailabilityService(self).validate_staff_overlap()
            except ValidationError as exc:
                errors.update(exc.message_dict)

        if self.service and self.start_time and self.end_time:
            try:
                AvailabilityService(self).validate_room_overlap()
            except ValidationError as exc:
                errors.update(exc.message_dict)

        if self.service and self.start_time and self.end_time:
            try:
                AvailabilityService(self).validate_equipment_overlap()
            except ValidationError as exc:
                errors.update(exc.message_dict)

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        staff_name = self.staff if self.staff else "Unassigned"

        return (
            f"{self.patient} with {staff_name} "
            f"@ {self.start_time:%Y-%m-%d %H:%M}"
        )

class AppointmentEvent(models.Model):
    """
    Stores important events that happen during an appointment lifecycle.

    This is an audit log for appointment changes such as:
    - status changes
    - staff changes
    - time changes
    - creation events
    """

    class EventType(models.TextChoices):
        CREATED = "created", "Created"
        STATUS_CHANGED = "status_changed", "Status Changed"
        STAFF_CHANGED = "staff_changed", "Staff Changed"
        TIME_CHANGED = "time_changed", "Time Changed"
        CANCELLED = "cancelled", "Cancelled"

    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name="events",
    )

    event_type = models.CharField(
        max_length=30,
        choices=EventType.choices,
    )

    old_value = models.CharField(
        max_length=255,
        blank=True,
    )

    new_value = models.CharField(
        max_length=255,
        blank=True,
    )

    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointment_events",
    )

    description = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["appointment", "created_at"]),
        ]

    def __str__(self):
        return (
            f"{self.appointment_id} - "
            f"{self.event_type}"
        )    