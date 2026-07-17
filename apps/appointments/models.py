from django.core.exceptions import ValidationError
from django.db import models

from core.models import TenantModel


class AppointmentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    CANCELLED = "cancelled", "Cancelled"


class Appointment(TenantModel):
    """
    `clinic` comes from TenantModel — not redeclared here. patient, staff,
    and service are each independently clinic-scoped (PatientProfile,
    StaffProfile, and Service are all TenantModel subclasses), so it's
    possible to construct an Appointment whose related objects belong to
    a *different* clinic than the appointment itself unless that's
    explicitly checked — see clean() below.

    clean() is not called automatically by save(); ModelForms and DRF
    ModelSerializers call it for you, but raw `Appointment.objects.create(...)`
    in scripts/shell/migrations does not. Call full_clean() explicitly in
    those contexts.
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

    class Meta:
        ordering = ["start_time"]
        indexes = [
            models.Index(fields=["clinic", "start_time"]),
            models.Index(fields=["staff", "start_time"]),
        ]

    def clean(self):
        super().clean()
        errors = {}

        if self.start_time and self.end_time and self.end_time <= self.start_time:
            errors["end_time"] = "End time must be after start time."

        for field_name in ("patient", "staff", "service"):
            related = getattr(self, field_name, None)
            if related is not None and related.clinic_id != self.clinic_id:
                errors[field_name] = "Must belong to the same clinic as the appointment."

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.patient} with {self.staff} @ {self.start_time:%Y-%m-%d %H:%M}"
