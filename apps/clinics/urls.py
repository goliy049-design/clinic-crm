from rest_framework.routers import DefaultRouter

from .views import ClinicViewSet

app_name = "clinics"

router = DefaultRouter()
router.register("", ClinicViewSet, basename="clinic")

urlpatterns = router.urls