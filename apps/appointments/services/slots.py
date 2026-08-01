from datetime import datetime, timedelta

from apps.staff.models import StaffSchedule


class SlotService:
    """
    Calculates available appointment slots for a given service,
    staff member and date.

    This service will become the single source of truth for
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
        Returns all possible appointment start times
        based on staff working shifts.
        """

        slots = []

        for shift in self.get_staff_shifts():
            slots.extend(
                self.generate_shift_slots(shift)
            )

        return slots
        
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
     
    def generate_shift_slots(self, shift):
        """
        Generate all possible slot start times inside one shift.
        """

        slots = []

        current = datetime.combine(
            self.date,
            shift.start_time,
        )

        shift_end = datetime.combine(
            self.date,
            shift.end_time,
        )

        duration = timedelta(
            minutes=self.service.duration_minutes,
        )

        while current + duration <= shift_end:
            slots.append(current)
            current += duration

        return slots    