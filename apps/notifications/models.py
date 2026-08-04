from django.conf import settings
from django.db import models

from core.models import TenantModel


class NotificationChannel(models.TextChoices):
    TELEGRAM = "telegram", "Telegram"
    SMS = "sms", "SMS"
    EMAIL = "email", "Email"
    IN_APP = "in_app", "In App"


class NotificationStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SENT = "sent", "Sent"
    FAILED = "failed", "Failed"
    READ = "read", "Read"


class Notification(TenantModel):
    """
    Represents a notification that can be delivered through one or more
    channels.

    Delivery is handled by NotificationService and channel providers.
    """

    title = models.CharField(
        max_length=255,
    )

    message = models.TextField()

    channel = models.CharField(
        max_length=20,
        choices=NotificationChannel.choices,
        default=NotificationChannel.IN_APP,
    )

    status = models.CharField(
        max_length=20,
        choices=NotificationStatus.choices,
        default=NotificationStatus.PENDING,
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    error_message = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["clinic", "status"]),
            models.Index(fields=["channel"]),
        ]

    def __str__(self):
        return self.title


class NotificationRecipient(models.Model):
    """
    Associates a notification with one recipient.

    Keeping recipients in a separate table allows one notification
    to be delivered to multiple users while tracking read status
    individually.
    """

    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name="recipients",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    is_read = models.BooleanField(
        default=False,
    )

    read_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = (
            "notification",
            "user",
        )

    def __str__(self):
        return (
            f"{self.user} - {self.notification.title}"
        )