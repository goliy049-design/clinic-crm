from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from apps.clinics.models import Clinic
from apps.appointments.services.appointment_creator import AppointmentCreator

from .appointment_serializers import (
    PublicAppointmentCreateSerializer,
)

from .patient_service import PublicPatientService


class PublicAppointmentCreateAPIView(APIView):
    """
    Create appointment from public channels.

    Used by:
    - Website
    - Telegram bot
    """

    permission_classes = [
        AllowAny,
    ]

    def post(self, request):

        clinic_slug = request.query_params.get(
            "clinic"
        )

        if not clinic_slug:
            return Response(
                {
                    "error": "clinic parameter is required"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        clinic = Clinic.objects.filter(
            slug=clinic_slug,
            is_active=True,
        ).first()

        if not clinic:
            return Response(
                {
                    "error": "clinic not found"
                },
                status=status.HTTP_404_NOT_FOUND,
            )


        serializer = PublicAppointmentCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )


        patient_data = serializer.validated_data["patient"]


        patient = PublicPatientService(
            clinic=clinic,
            phone_number=patient_data["phone_number"],
            first_name=patient_data["first_name"],
            last_name=patient_data["last_name"],
        ).get_or_create()


        appointment = AppointmentCreator(
            clinic=clinic,
            patient=patient,
            service=serializer.validated_data["service"],
            staff=serializer.validated_data.get("staff"),
            start_time=serializer.validated_data["start_time"],
            source="website",
        ).create()


        return Response(
            {
                "success": True,
                "appointment_id": appointment.id,
                "status": appointment.status,
            },
            status=status.HTTP_201_CREATED,
        )