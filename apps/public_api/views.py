from datetime import date

from apps.appointments.services.slots import SlotService
from apps.staff.models import StaffProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.clinics.models import Clinic
from apps.services.models import ServiceVariant
from apps.staff.models import StaffProfile

from .serializers import (
    PublicServiceSerializer,
    PublicStaffSerializer,
    PublicSlotSerializer,
)


class PublicServiceListAPIView(APIView):

    permission_classes = [
        AllowAny
    ]

    def get(self, request):

        clinic_slug = request.query_params.get(
            "clinic"
        )

        if not clinic_slug:
            return Response(
                {
                    "error": "clinic parameter is required"
                },
                status=400,
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
                status=404,
            )

        services = ServiceVariant.objects.filter(
            clinic=clinic,
            is_active=True,
        ).select_related(
            "service"
        )

        serializer = PublicServiceSerializer(
            services,
            many=True,
        )

        return Response(
            serializer.data
        )


class PublicStaffListAPIView(APIView):

    permission_classes = [
        AllowAny
    ]

    def get(self, request):

        clinic_slug = request.query_params.get(
            "clinic"
        )

        service_id = request.query_params.get(
            "service"
        )

        if not clinic_slug or not service_id:
            return Response(
                {
                    "error": "clinic and service parameters are required"
                },
                status=400,
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
                status=404,
            )

        staff = StaffProfile.objects.filter(
            clinic=clinic,
            is_active=True,
            staff_services__service_id=service_id,
            staff_services__is_active=True,
        ).select_related(
            "user"
        ).distinct()

        serializer = PublicStaffSerializer(
            staff,
            many=True,
        )

        return Response(
            serializer.data
        )

class PublicAvailableSlotsAPIView(APIView):

    permission_classes = [
        AllowAny
    ]

    def get(self, request):

        clinic_slug = request.query_params.get(
            "clinic"
        )

        service_id = request.query_params.get(
            "service"
        )

        staff_id = request.query_params.get(
            "staff"
        )

        selected_date = request.query_params.get(
            "date"
        )

        if not all([
            clinic_slug,
            service_id,
            staff_id,
            selected_date,
        ]):
            return Response(
                {
                    "error": "clinic, service, staff and date are required"
                },
                status=400,
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
                status=404,
            )


        service = ServiceVariant.objects.filter(
            id=service_id,
            clinic=clinic,
            is_active=True,
        ).first()


        if not service:
            return Response(
                {
                    "error": "service not found"
                },
                status=404,
            )


        staff = StaffProfile.objects.filter(
            id=staff_id,
            clinic=clinic,
            is_active=True,
        ).first()


        if not staff:
            return Response(
                {
                    "error": "staff not found"
                },
                status=404,
            )


        slots = SlotService(
            clinic=clinic,
            service=service,
            staff=staff,
            date=date.fromisoformat(
                selected_date
            ),
        ).get_available_slots()


        return Response(
            [
                slot.strftime("%H:%M")
                for slot in slots
            ]
        )    