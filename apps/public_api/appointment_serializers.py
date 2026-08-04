from rest_framework import serializers

from apps.services.models import ServiceVariant
from apps.staff.models import StaffProfile


class PublicPatientInputSerializer(serializers.Serializer):
    """
    Patient information received from public channels.
    """

    first_name = serializers.CharField(
        max_length=150
    )

    last_name = serializers.CharField(
        max_length=150
    )

    phone_number = serializers.CharField(
        max_length=32
    )


class PublicAppointmentCreateSerializer(serializers.Serializer):
    """
    Public appointment creation request.

    Used by:
    - Website
    - Telegram bot
    """

    patient = PublicPatientInputSerializer()

    service = serializers.PrimaryKeyRelatedField(
        queryset=ServiceVariant.objects.all()
    )

    staff = serializers.PrimaryKeyRelatedField(
        queryset=StaffProfile.objects.all(),
        required=False,
        allow_null=True,
    )

    start_time = serializers.DateTimeField()