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

    slot = serializers.DateTimeField(
        format="%H:%M",
    )        