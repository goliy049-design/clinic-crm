from django.core.exceptions import ValidationError

from apps.staff.models import StaffSchedule


class AvailabilityService:
    """
    Central service responsible for appointment availability checks.
    """

    def __init__(self, appointment):
        self.appointment = appointment

    def staff_is_available(self):
        if not self.appointment.staff:
            return True

        return StaffSchedule.objects.filter(
            staff=self.appointment.staff,
            date=self.appointment.start_time.date(),
            is_available=True,
            start_time__lte=self.appointment.start_time.time(),
            end_time__gte=self.appointment.end_time.time(),
        ).exists()

    def validate_staff_schedule(self):
        if not self.staff_is_available():
            raise ValidationError({
                "start_time": (
                    "Staff member is not available during this time."
                )
            })

    def validate_staff_overlap(self):
        """
        Validate that the selected staff member has no overlapping appointment.
        """
        from apps.appointments.models import (
            Appointment,
            AppointmentStatus,
        )

        if not self.appointment.staff:
            return

        overlapping = Appointment.objects.filter(
            staff=self.appointment.staff,
            start_time__lt=self.appointment.end_time,
            end_time__gt=self.appointment.start_time,
        ).exclude(
            status__in=[
                AppointmentStatus.CANCELLED,
                AppointmentStatus.NO_SHOW,
            ]
        )

        if self.appointment.pk:
            overlapping = overlapping.exclude(
                pk=self.appointment.pk,
            )

        if overlapping.exists():
            raise ValidationError({
                "start_time": (
                    "Staff member already has another appointment during this time."
                )
            })


    def validate_room_overlap(self):
        """
        Validate that every required room is free during
        the requested appointment time.
        """
        from apps.appointments.models import (
            Appointment,
            AppointmentStatus,
        )

        if not self.appointment.service:
            return

        requested_rooms = (
            self.appointment.service.equipment.exclude(
                room__isnull=True,
            )
            .values_list(
                "room_id",
                flat=True,
            )
            .distinct()
        )

        if not requested_rooms:
            return

        overlapping = Appointment.objects.filter(
            start_time__lt=self.appointment.end_time,
            end_time__gt=self.appointment.start_time,
            service__equipment__room_id__in=requested_rooms,
        ).exclude(
            status__in=[
                AppointmentStatus.CANCELLED,
                AppointmentStatus.NO_SHOW,
            ]
        ).distinct()

        if self.appointment.pk:
            overlapping = overlapping.exclude(
                pk=self.appointment.pk,
            )

        if overlapping.exists():
            raise ValidationError({
                "service": (
                    "Required room is already occupied during this time."
                )
            })        