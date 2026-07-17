from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = "services"

router = DefaultRouter()
# router.register("services", SomeViewSet, basename="services")

urlpatterns = router.urls
