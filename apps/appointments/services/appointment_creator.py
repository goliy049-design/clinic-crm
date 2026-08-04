from datetime import timedelta

from django.core.exceptions import ValidationError

from apps.appointments.models import (
    Appointment,
    AppointmentEvent,
)
from apps.appointments.services.slots import SlotService


class AppointmentCreator:
    """
    Central service for creating appointments.

    Used by:
    - Admin panel
    - Website
    - Telegram bot
    """

    def __init__(
        self,
        clinic,
        patient,
        service,
        start_time,
        staff=None,
        source="admin_panel",
        notes="",
    ):
        self.clinic = clinic
        self.patient = patient
        self.service = service
        self.start_time = start_time
        self.staff = staff
        self.source = source
        self.notes = notes

    def validate_slot(self):
        """
        Check if selected time is available.
        """

        if not self.staff:
            return

        slots = SlotService(
            clinic=self.clinic,
            service=self.service,
            staff=self.staff,
            date=self.start_time.date(),
        ).get_available_slots()

        if not any(
            slot.replace(second=0, microsecond=0)
            ==
            self.start_time.replace(second=0, microsecond=0)
            for slot in slots
        ):
            raise ValidationError(
                "Selected time is not available."
            )

    def create(self):
        """
        Create appointment.
        """

        self.validate_slot()

        appointment = Appointment(
            clinic=self.clinic,
            patient=self.patient,
            staff=self.staff,
            service=self.service,
            start_time=self.start_time,
            source=self.source,
            notes=self.notes,
        )

        appointment.end_time = (
            self.start_time
            + timedelta(
                minutes=(
                    self.service.duration_minutes
                    + self.service.buffer_minutes
                )
            )
        )

        appointment.full_clean()
        appointment.save()

        AppointmentEvent.objects.create(
            appointment=appointment,
            event_type=AppointmentEvent.EventType.CREATED,
            description="Appointment created",
        )

        return appointment