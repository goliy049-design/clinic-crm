from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = "staff"

router = DefaultRouter()
# router.register("staff", SomeViewSet, basename="staff")

urlpatterns = router.urls
