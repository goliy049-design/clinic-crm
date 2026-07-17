from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = "payments"

router = DefaultRouter()
# router.register("payments", SomeViewSet, basename="payments")

urlpatterns = router.urls
