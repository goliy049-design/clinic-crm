from rest_framework import serializers

from .models import StaffProfile, StaffService


class StaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffProfile
        fields = [
            "id",
            "user",
            "role",
            "is_active",
            "clinic",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class StaffServiceSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(
        source="staff.user.username",
        read_only=True,
    )

    service_name = serializers.CharField(
        source="service.name",
        read_only=True,
    )

    class Meta:
        model = StaffService
        fields = [
            "id",
            "staff",
            "staff_name",
            "service",
            "service_name",
            "duration_minutes",
            "price",
            "is_active",
            "clinic",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "clinic",
            "created_at",
            "updated_at",
        ]