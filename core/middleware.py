"""
Resolves which Clinic the current request belongs to and makes it
available two ways:

1. `request.clinic` — for views/admin code that wants it directly.
2. core.context's contextvar — so core.managers.TenantManager can scope
   every `Model.objects` query automatically, without each view having
   to remember to filter by clinic.

Resolution order: a staff member's clinic comes from their StaffProfile;
a patient-portal user's clinic comes from their PatientProfile. Anonymous
requests, superusers with no profile, and management commands simply get
`clinic = None`, which makes TenantManager fall back to unfiltered (the
`unscoped`-equivalent) behaviour — appropriate for platform-level admin,
but means application code should not rely on implicit scoping for
unauthenticated endpoints.
"""
from core.context import clear_current_clinic_id, set_current_clinic_id


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        clinic = self._resolve_clinic(request)
        request.clinic = clinic

        if clinic is not None:
            set_current_clinic_id(clinic.id)

        try:
            response = self.get_response(request)
        finally:
            clear_current_clinic_id()

        return response

    @staticmethod
    def _resolve_clinic(request):
        user = getattr(request, "user", None)
        if user is None or not user.is_authenticated:
            return None

        staff_profile = getattr(user, "staff_profile", None)
        if staff_profile is not None:
            return staff_profile.clinic

        patient_profile = getattr(user, "patient_profile", None)
        if patient_profile is not None:
            return patient_profile.clinic

        return None
