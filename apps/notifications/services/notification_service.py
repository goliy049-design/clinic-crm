from django.contrib.auth import get_user_model

from apps.notifications.models import (
    Notification,
    NotificationRecipient,
    NotificationStatus,
)


User = get_user_model()


class NotificationService:
    """
    Handles creation and management of notifications.

    This service does not send messages.
    Delivery providers (Telegram, SMS, Email) will be added later.
    """

    @staticmethod
    def create_notification(
        *,
        clinic,
        title,
        message,
        recipients,
        channel,
    ):
        """
        Creates a notification and assigns recipients.

        recipients:
            list/queryset of User objects
        """

        notification = Notification.objects.create(
            clinic=clinic,
            title=title,
            message=message,
            channel=channel,
            status=NotificationStatus.PENDING,
        )

        NotificationRecipient.objects.bulk_create(
            [
                NotificationRecipient(
                    notification=notification,
                    user=user,
                )
                for user in recipients
            ]
        )

        return notification