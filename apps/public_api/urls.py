from django.urls import path

from .views import (
    PublicServiceListAPIView,
    PublicStaffListAPIView,
    PublicAvailableSlotsAPIView,
)

from .appointment_views import (
    PublicAppointmentCreateAPIView,
)


app_name = "public_api"


urlpatterns = [

    path(
        "services/",
        PublicServiceListAPIView.as_view(),
        name="public-services",
    ),

    path(
        "staff/",
        PublicStaffListAPIView.as_view(),
        name="public-staff",
    ),

    path(
        "slots/",
        PublicAvailableSlotsAPIView.as_view(),
        name="public-slots",
    ),

    path(
        "appointments/",
        PublicAppointmentCreateAPIView.as_view(),
        name="public-create-appointment",
    ),
]