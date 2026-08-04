from django.utils import timezone

from apps.notifications.models import (
    NotificationQueue,
    NotificationQueueStatus,
    NotificationRule,
    Notification,
    NotificationStatus,
)


class NotificationEngine:
    """
    Decides how appointment/system events
    should create notifications.
    """

    @staticmethod
    def process_event(*, event, recipients):
        """
        Process an event and create either
        a queue item or a direct notification.
        """

        rule = NotificationRule.objects.filter(
            clinic=event.appointment.clinic,
            event_type=event.event_type,
            is_active=True,
        ).first()

        if not rule:
            return None

        if rule.approval_required:
            return NotificationQueue.objects.create(
                clinic=event.appointment.clinic,
                event_type=event.event_type,
                reference_id=event.id,
                recipient_type=rule.recipient_type,
                title="Notification Pending Approval",
                message="Notification waiting for approval.",
                channel=rule.channel,
                status=NotificationQueueStatus.PENDING,
            )

        return Notification.objects.create(
            clinic=event.appointment.clinic,
            title="Appointment Notification",
            message="Notification created from event.",
            channel=rule.channel,
            status=NotificationStatus.PENDING,
        )

    @staticmethod
    def approve_queue(queue: NotificationQueue):
        """
        Approves a queued notification
        and creates the real notification.
        """

        if queue.status != NotificationQueueStatus.PENDING:
            return None

        notification = Notification.objects.create(
            clinic=queue.clinic,
            title=queue.title,
            message=queue.message,
            channel=queue.channel,
            status=NotificationStatus.PENDING,
        )

        queue.status = NotificationQueueStatus.APPROVED
        queue.approved_at = timezone.now()
        queue.save(
            update_fields=[
                "status",
                "approved_at",
            ]
        )

        return notification