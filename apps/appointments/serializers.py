from rest_framework import serializers

from .models import Appointment, AppointmentStatus


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