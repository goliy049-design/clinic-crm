from datetime import datetime, timedelta
from django.utils import timezone

from apps.staff.models import StaffSchedule


class SlotService:
    """
    Calculates available appointment slots for a given service,
    staff member and date.

    This service is the single source of truth for
    appointment availability across:

    - Admin panel
    - Website
    - Telegram bot
    """

    def __init__(
        self,
        clinic,
        service,
        date,
        staff=None,
    ):
        self.clinic = clinic
        self.service = service
        self.date = date
        self.staff = staff

    def get_available_slots(self):
        """
        Returns available appointment start times.
        """

        slots = []

        for shift in self.get_staff_shifts():
            slots.extend(
                self.generate_shift_slots(shift)
            )

        return self.remove_booked_slots(slots)

    def get_staff_shifts(self):
        """
        Returns all working shifts of the selected staff member
        for the requested date.
        """

        if not self.staff:
            return StaffSchedule.objects.none()

        return StaffSchedule.objects.filter(
            clinic=self.clinic,
            staff=self.staff,
            date=self.date,
            is_available=True,
        ).order_by(
            "start_time",
        )

    def get_total_duration(self):
        """
        Returns total occupied time of the appointment.

        Includes:
        - treatment duration
        - preparation/cleaning buffer
        """

        return timedelta(
            minutes=(
                self.service.duration_minutes
                + self.service.buffer_minutes
            )
        )

    def generate_shift_slots(self, shift):
        """
        Generate all possible appointment start times
        inside one working shift.
        """

        slots = []

        current = timezone.make_aware(
            datetime.combine(
              self.date,
              shift.start_time,
            )
        )

        shift_end = timezone.make_aware(
            datetime.combine(
                self.date,
                shift.end_time,
            )
        )

        duration = self.get_total_duration()

        while current + duration <= shift_end:
            slots.append(current)
            current += duration

        return slots

    def remove_booked_slots(self, slots):
        """
        Removes slots that overlap with existing appointments.
        """

        from apps.appointments.models import (
            Appointment,
            AppointmentStatus,
        )

        if not self.staff:
            return slots

        appointments = Appointment.objects.filter(
            clinic=self.clinic,
            staff=self.staff,
            start_time__date=self.date,
        ).exclude(
            status__in=[
                AppointmentStatus.CANCELLED,
                AppointmentStatus.NO_SHOW,
            ]
        )

        duration = self.get_total_duration()

        available_slots = []

        for slot in slots:
            slot_end = slot + duration

            has_conflict = appointments.filter(
                start_time__lt=slot_end,
                end_time__gt=slot,
            ).exists()

            if not has_conflict:
                available_slots.append(slot)

        return available_slots