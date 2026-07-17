from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = "patients"

router = DefaultRouter()
# router.register("patients", SomeViewSet, basename="patients")

urlpatterns = router.urls
