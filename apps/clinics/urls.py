from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = "clinics"

router = DefaultRouter()
# router.register("clinics", SomeViewSet, basename="clinics")

urlpatterns = router.urls
