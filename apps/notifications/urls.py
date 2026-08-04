from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.notifications.views import (
    NotificationQueueViewSet,
)


app_name = "notifications"


router = DefaultRouter()

router.register(
    "queue",
    NotificationQueueViewSet,
    basename="notification-queue",
)


urlpatterns = router.urls
