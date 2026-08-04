from rest_framework import serializers

from apps.services.models import ServiceVariant
from apps.staff.models import StaffProfile


class PublicServiceSerializer(serializers.ModelSerializer):

    service_name = serializers.CharField(
        source="service.name",
        read_only=True,
    )

    class Meta:
        model = ServiceVariant

        fields = [
            "id",
            "service_name",
            "name",
            "duration_minutes",
            "price",
        ]


class PublicStaffSerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    class Meta:
        model = StaffProfile

        fields = [
            "id",
            "name",
            "role",
        ]


class PublicSlotSerializer(serializers.Serializer):

    time = serializers.CharField()

from apps.clinics.models import Clinic
from apps.staff.models import StaffProfile
from apps.patients.models import PatientProfile


class PublicBookingSerializer(serializers.Serializer):

    clinic = serializers.SlugRelatedField(
        queryset=Clinic.objects.filter(
            is_active=True
        ),
        slug_field="slug",
    )

    patient_name = serializers.CharField(
        max_length=255
    )

    phone_number = serializers.CharField(
        max_length=32
    )

    service = serializers.PrimaryKeyRelatedField(
        queryset=ServiceVariant.objects.all()
    )

    staff = serializers.PrimaryKeyRelatedField(
        queryset=StaffProfile.objects.all()
    )

    start_time = serializers.DateTimeField()   