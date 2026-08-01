from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AppointmentViewSet,
    AvailableSlotsAPIView,
)


app_name = "appointments"


router = DefaultRouter()

router.register(
    "",
    AppointmentViewSet,
    basename="appointments",
)


urlpatterns = [
    path(
        "available-slots/",
        AvailableSlotsAPIView.as_view(),
        name="available-slots",
    ),
] + router.urls