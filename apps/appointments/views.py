from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentViewSet(ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(
            clinic=self.request.user.staff_profile.clinic
        )

    def perform_create(self, serializer):
        serializer.save(
            clinic=self.request.user.staff_profile.clinic
        )