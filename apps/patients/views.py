from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import PatientProfile
from .serializers import PatientSerializer


class PatientViewSet(ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
       return PatientProfile.objects.filter(
          clinic=self.request.user.staff_profile.clinic
       )

    def perform_create(self, serializer):
        serializer.save(
            clinic=self.request.user.staff_profile.clinic
        )