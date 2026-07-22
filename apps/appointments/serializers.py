from rest_framework import serializers

from .models import Appointment


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
            "created_at",
            "updated_at",
        ]