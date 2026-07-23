from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import StaffProfile, StaffService
from .serializers import (
    StaffProfileSerializer,
    StaffServiceSerializer,
)


class StaffProfileViewSet(ModelViewSet):
    serializer_class = StaffProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StaffProfile.objects.filter(
            clinic=self.request.user.staff_profile.clinic
        )

    def perform_create(self, serializer):
        serializer.save(
            clinic=self.request.user.staff_profile.clinic
        )


class StaffServiceViewSet(ModelViewSet):
    serializer_class = StaffServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StaffService.objects.filter(
            clinic=self.request.user.staff_profile.clinic
        )

    def perform_create(self, serializer):
        serializer.save(
            clinic=self.request.user.staff_profile.clinic
        )
