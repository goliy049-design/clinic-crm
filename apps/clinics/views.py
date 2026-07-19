from rest_framework import permissions
from rest_framework import viewsets

from .models import Clinic
from .serializers import ClinicSerializer


class ClinicViewSet(viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    permission_classes = [permissions.IsAuthenticated]
