from django.contrib import admin

from apps.notifications.models import (
    Notification,
    NotificationRecipient,
    NotificationRule,
    NotificationTemplate,
    NotificationQueue,
)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "channel",
        "status",
        "clinic",
        "created_at",
    )

    list_filter = (
        "channel",
        "status",
        "clinic",
    )


@admin.register(NotificationRecipient)
class NotificationRecipientAdmin(admin.ModelAdmin):
    list_display = (
        "notification",
        "user",
        "is_read",
    )


@admin.register(NotificationRule)
class NotificationRuleAdmin(admin.ModelAdmin):
    list_display = (
        "event_type",
        "recipient_type",
        "channel",
        "approval_required",
        "is_active",
        "clinic",
    )

    list_filter = (
        "approval_required",
        "is_active",
        "channel",
        "clinic",
    )


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "event_type",
        "channel",
        "is_active",
        "clinic",
    )

    list_filter = (
        "event_type",
        "channel",
        "is_active",
        "clinic",
    )


@admin.register(NotificationQueue)
class NotificationQueueAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "event_type",
        "status",
        "channel",
        "clinic",
        "created_at",
    )

    list_filter = (
        "status",
        "channel",
        "clinic",
    )