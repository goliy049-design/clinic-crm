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

        notification = Notification.objects.create(
            clinic=event.appointment.clinic,
            title="Appointment Notification",
            message="Notification created from event.",
            channel=rule.channel,
            status=NotificationStatus.PENDING,
        )

        return notification