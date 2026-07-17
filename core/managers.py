"""
Managers backing core.models.TenantModel.

Design: this is row-level, shared-schema multi-tenancy (one Postgres
database, every tenant-owned table has a `clinic_id` column) rather than
schema-per-tenant. It's the right default for this stage of the project;
if true hard isolation is ever needed, swap this layer for
schema-per-tenant without touching call sites, since application code
only ever talks to `Model.objects`, never raw filters on `clinic`.

- `TenantManager` (assigned to `objects` on every TenantModel subclass)
  automatically filters by the clinic set on the current request by
  TenantMiddleware. This is the safe default: a viewset/service that
  forgets to filter by clinic still can't leak another tenant's rows.
- `UnscopedManager` (assigned to `unscoped`) is the explicit escape hatch
  for code that legitimately needs cross-tenant access: platform-admin
  tooling, Celery beat jobs that sweep all clinics, data migrations.
  Using it should always be a deliberate, reviewable choice.
"""
from django.db import models

from core.context import get_current_clinic_id


class TenantQuerySet(models.QuerySet):
    def for_clinic(self, clinic):
        """Explicitly scope to a given clinic (accepts a Clinic instance or id)."""
        return self.filter(clinic=clinic)


class TenantManager(models.Manager):
    def get_queryset(self):
        qs = TenantQuerySet(self.model, using=self._db)
        clinic_id = get_current_clinic_id()
        if clinic_id is not None:
            qs = qs.filter(clinic_id=clinic_id)
        return qs


class UnscopedManager(models.Manager):
    def get_queryset(self):
        return TenantQuerySet(self.model, using=self._db)
