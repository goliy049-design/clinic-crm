from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError

from apps.services.models import ServiceVariant
from apps.staff.models import StaffProfile

from .models import Appointment, AppointmentEvent
from .serializers import (
    AppointmentSerializer,
    AppointmentEventSerializer,
    AvailableSlotSerializer,
    ChangeAppointmentStatusSerializer,
)
from .services.slots import SlotService
from .services.appointment_service import AppointmentService


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

    @action(
        detail=True,
        methods=["post"],
        url_path="change-status",
    )
    def change_status(self, request, pk=None):
        appointment = self.get_object()

        serializer = ChangeAppointmentStatusSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        new_status = serializer.validated_data["status"]

        note = serializer.validated_data.get(
            "note",
            "",
        )

        AppointmentService(
            appointment
        ).change_status(
            new_status=new_status,
            changed_by=request.user,
            note=note,
        )

        return Response(
            AppointmentSerializer(
                appointment
            ).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["get"],
        url_path="events",
    )
    def events(self, request, pk=None):
        appointment = self.get_object()

        events = AppointmentEvent.objects.filter(
            appointment=appointment
        ).order_by(
            "created_at"
        )

        serializer = AppointmentEventSerializer(
            events,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class AvailableSlotsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = AvailableSlotSerializer(
            data=request.query_params
        )

        serializer.is_valid(
            raise_exception=True
        )

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