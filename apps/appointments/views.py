from datetime import datetime

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError

from apps.services.models import ServiceVariant
from apps.staff.models import StaffProfile

from .models import Appointment
from .serializers import (
    AppointmentSerializer,
    AvailableSlotSerializer,
)
from .services.slots import SlotService


class AppointmentViewSet(ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(
            clinic=self.request.user.staff_profile.clinic
        )

    def perform_create(self, serializer):
        clinic = self.request.user.staff_profile.clinic

        service = serializer.validated_data["service"]
        staff = serializer.validated_data.get("staff")
        start_time = serializer.validated_data["start_time"]

        if staff:
            slots = SlotService(
                clinic=clinic,
                service=service,
                staff=staff,
                date=start_time.date(),
            ).get_available_slots()

            valid_slot = any(
                slot == start_time
                for slot in slots
            )

            if not valid_slot:
                raise ValidationError(
                    "Selected time is not available."
                )

        serializer.save(
            clinic=clinic
        )


class AvailableSlotsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = AvailableSlotSerializer(
            data=request.query_params
        )

        serializer.is_valid(raise_exception=True)

        clinic = request.user.staff_profile.clinic

        service = ServiceVariant.objects.get(
            id=serializer.validated_data["service"],
            clinic=clinic,
        )

        staff = StaffProfile.objects.get(
            id=serializer.validated_data["staff"],
            clinic=clinic,
        )

        slots = SlotService(
            clinic=clinic,
            service=service,
            staff=staff,
            date=serializer.validated_data["date"],
        ).get_available_slots()

        return Response(
            [
                slot.strftime("%H:%M")
                for slot in slots
            ],
            status=status.HTTP_200_OK,
        )