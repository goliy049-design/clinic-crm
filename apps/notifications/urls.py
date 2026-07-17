from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = "notifications"

router = DefaultRouter()
# router.register("notifications", SomeViewSet, basename="notifications")

urlpatterns = router.urls
