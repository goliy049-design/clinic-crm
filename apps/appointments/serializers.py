from rest_framework import serializers

from .models import (
    Appointment,
    AppointmentStatus,
    AppointmentEvent,
)


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment

        fields = [
            "id",
            "patient",
            "staff",
            "service",
            "start_time",
            "end_time",
            "status",
            "source",
            "notes",
            "clinic",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "clinic",
            "status",
            "created_at",
            "updated_at",
        ]


class AppointmentEventSerializer(serializers.ModelSerializer):
    """
    Serializer for appointment timeline events.
    """

    created_by_name = serializers.CharField(
        source="created_by.username",
        read_only=True,
    )

    class Meta:
        model = AppointmentEvent

        fields = [
            "id",
            "event_type",
            "old_value",
            "new_value",
            "description",
            "created_by",
            "created_by_name",
            "created_at",
        ]

        read_only_fields = fields


class ChangeAppointmentStatusSerializer(serializers.Serializer):
    """
    Serializer for controlled appointment status transitions.
    """

    status = serializers.ChoiceField(
        choices=AppointmentStatus.choices,
    )

    note = serializers.CharField(
        required=False,
        allow_blank=True,
    )


class AvailableSlotSerializer(serializers.Serializer):
    """
    Input serializer for available appointment slots API.
    """

    service = serializers.UUIDField()
    staff = serializers.UUIDField()
    date = serializers.DateField()