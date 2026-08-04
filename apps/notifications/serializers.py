from rest_framework import serializers

from apps.notifications.models import NotificationQueue


class NotificationQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationQueue
        fields = [
            "id",
            "event_type",
            "title",
            "message",
            "status",
            "scheduled_at",
            "approved_at",
            "cancelled_at",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "approved_at",
            "cancelled_at",
        ]