from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = "medical_records"

router = DefaultRouter()
# router.register("medical-records", SomeViewSet, basename="medical-records")

urlpatterns = router.urls
