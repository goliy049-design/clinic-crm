from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from .models import Service
from .serializers import ServiceSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Service.objects.filter(
            clinic=self.request.user.staff_profile.clinic
        )

    def perform_create(self, serializer):
        serializer.save(
            clinic=self.request.user.staff_profile.clinic
        )