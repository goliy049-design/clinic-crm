from django.utils import timezone

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.notifications.models import (
    NotificationQueue,
    NotificationQueueStatus,
)

from apps.notifications.serializers import (
    NotificationQueueSerializer,
)


class NotificationQueueViewSet(viewsets.ModelViewSet):
    """
    Manage notification approval queue.

    Sensitive notifications require approval before delivery.
    """

    serializer_class = NotificationQueueSerializer

    def get_queryset(self):
        return NotificationQueue.objects.filter(
            clinic=self.request.user.staff_profile.clinic
        )

    @action(
        detail=True,
        methods=["post"],
    )
    def approve(self, request, pk=None):
        queue_item = self.get_object()

        if queue_item.status != NotificationQueueStatus.PENDING:
            return Response(
                {
                    "detail": "Only pending notifications can be approved."
                },
                status=400,
            )

        queue_item.status = NotificationQueueStatus.APPROVED
        queue_item.approved_at = timezone.now()
        queue_item.save()

        return Response(
            NotificationQueueSerializer(queue_item).data
        )

    @action(
        detail=True,
        methods=["post"],
    )
    def cancel(self, request, pk=None):
        queue_item = self.get_object()

        if queue_item.status != NotificationQueueStatus.PENDING:
            return Response(
                {
                    "detail": "Only pending notifications can be cancelled."
                },
                status=400,
            )

        queue_item.status = NotificationQueueStatus.CANCELLED
        queue_item.cancelled_at = timezone.now()
        queue_item.save()

        return Response(
            NotificationQueueSerializer(queue_item).data
        )