from rest_framework.routers import DefaultRouter

from .views import (
    StaffProfileViewSet,
    StaffServiceViewSet,
)

app_name = "staff"

router = DefaultRouter()

router.register(
    "staff-services",
    StaffServiceViewSet,
    basename="staff-services",
)

router.register(
    "",
    StaffProfileViewSet,
    basename="staff",
)

urlpatterns = router.urls