from django.core.exceptions import ValidationError
from django.db import transaction

from apps.appointments.models import (
    Appointment,
    AppointmentEvent,
)


class AppointmentService:
    """
    Domain service responsible for appointment business operations.
    """

    def __init__(self, appointment: Appointment):
        self.appointment = appointment

    @transaction.atomic
    def change_status(
        self,
        *,
        new_status: str,
        changed_by=None,
        note: str = "",
    ):
        old_status = self.appointment.status

        allowed_statuses = (
            Appointment.ALLOWED_STATUS_TRANSITIONS.get(
                old_status,
                set(),
            )
        )

        if new_status not in allowed_statuses:
            raise ValidationError(
                {
                    "status": (
                        f"Cannot change status "
                        f"from '{old_status}' "
                        f"to '{new_status}'."
                    )
                }
            )

        self.appointment.status = new_status
        self.appointment.save()

        AppointmentEvent.objects.create(
            appointment=self.appointment,
            event_type=AppointmentEvent.EventType.STATUS_CHANGED,
            old_value=old_status,
            new_value=new_status,
            created_by=changed_by,
            description=note,
        )

        return self.appointment