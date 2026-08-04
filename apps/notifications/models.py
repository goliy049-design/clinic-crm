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

class NotificationRule(TenantModel):
    """
    Defines how an event should create a notification.

    Rules can be global or clinic-specific.
    """

    event_type = models.CharField(
        max_length=100,
    )

    recipient_type = models.CharField(
        max_length=50,
    )

    channel = models.CharField(
        max_length=20,
        choices=NotificationChannel.choices,
        default=NotificationChannel.IN_APP,
    )

    approval_required = models.BooleanField(
        default=False,
    )

    delay_minutes = models.PositiveIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["event_type"]
        indexes = [
            models.Index(fields=["clinic", "event_type"]),
            models.Index(fields=["event_type", "is_active"]),
        ]

    def __str__(self):
        return self.event_type    

class NotificationTemplate(TenantModel):
    """
    Stores customizable notification message templates.

    Templates can be clinic-specific and support multiple channels.
    """

    name = models.CharField(
        max_length=100,
    )

    event_type = models.CharField(
        max_length=100,
    )

    channel = models.CharField(
        max_length=20,
        choices=NotificationChannel.choices,
        default=NotificationChannel.IN_APP,
    )

    title_template = models.CharField(
        max_length=255,
    )

    message_template = models.TextField()

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["event_type", "channel"]
        indexes = [
            models.Index(fields=["clinic", "event_type"]),
            models.Index(fields=["event_type", "channel"]),
        ]

    def __str__(self):
        return self.name   

class NotificationQueueStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    CANCELLED = "cancelled", "Cancelled"
    SENT = "sent", "Sent"


class NotificationQueue(TenantModel):
    """
    Stores notifications waiting for approval or delivery.
    Used for sensitive actions where operators may need time to correct mistakes.
    """

    event_type = models.CharField(
        max_length=100,
    )

    reference_id = models.UUIDField(
        null=True,
        blank=True,
    )

    recipient_type = models.CharField(
        max_length=50,
    )

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
        choices=NotificationQueueStatus.choices,
        default=NotificationQueueStatus.PENDING,
    )

    scheduled_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    cancelled_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["clinic", "status"]),
            models.Index(fields=["event_type"]),
        ]

    def __str__(self):
        return self.title