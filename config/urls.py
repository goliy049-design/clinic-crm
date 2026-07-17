from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/clinics/", include("apps.clinics.urls")),
    path("api/v1/patients/", include("apps.patients.urls")),
    path("api/v1/staff/", include("apps.staff.urls")),
    path("api/v1/services/", include("apps.services.urls")),
    path("api/v1/appointments/", include("apps.appointments.urls")),
    path("api/v1/payments/", include("apps.payments.urls")),
    path("api/v1/medical-records/", include("apps.medical_records.urls")),
    path("api/v1/media/", include("apps.media.urls")),
    path("api/v1/notifications/", include("apps.notifications.urls")),
    path("api/v1/integrations/", include("apps.integrations.urls")),
]
