"""
Base ModelAdmin for TenantModel subclasses. core.managers.TenantManager
already scopes `objects` by the request's clinic, but Django admin builds
its querysets in ways that can bypass that (e.g. `model._default_manager`
combined with explicit list/search), so this adds a second, explicit
layer at the admin boundary itself — never rely on a single layer for
tenant isolation.
"""
from django.contrib import admin


class TenantScopedAdmin(admin.ModelAdmin):
    """
    - Superusers see every clinic's records (needed for platform support).
    - Everyone else only sees/edits rows belonging to their own clinic
      (resolved by TenantMiddleware onto `request.clinic`); if no clinic
      could be resolved, they see nothing rather than everything.
    - New objects created in admin are auto-assigned to the request's
      clinic, so a staff user can never accidentally create a record
      under the wrong tenant.
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        clinic = getattr(request, "clinic", None)
        return qs.filter(clinic=clinic) if clinic else qs.none()

    def save_model(self, request, obj, form, change):
        if not change and not request.user.is_superuser:
            obj.clinic = getattr(request, "clinic", None)
        super().save_model(request, obj, form, change)
