from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = "accounts"

router = DefaultRouter()
# router.register("users", SomeViewSet, basename="users")

urlpatterns = router.urls
