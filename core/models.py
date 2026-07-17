import uuid

from django.db import models
from django.utils import timezone

from core.managers import TenantManager, UnscopedManager


class BaseModel(models.Model):
    """
    Abstract base model providing a UUID primary key and timestamps.
    All models across apps should inherit from this (directly, or via
    TenantModel below) for consistency.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class TenantModel(BaseModel):
    """
    Abstract base model for every clinic-owned (tenant) record.

    This is the multi-tenancy boundary for the whole project: every
    business model — patients, appointments, payments, medical records,
    notifications, etc. — must inherit from TenantModel instead of
    BaseModel directly, so it is physically impossible to create a
    business record that isn't attached to a Clinic.

    `objects` is tenant-scoped by default (see core.managers.TenantManager):
    it automatically filters by whatever clinic TenantMiddleware attached
    to the current request, so a viewset that simply does
    `Model.objects.all()` can never leak another clinic's rows. Use the
    `unscoped` manager only for deliberate cross-tenant operations
    (platform admin tooling, scheduled jobs that sweep every clinic).

    Example (future business model, not created yet):
        class Appointment(TenantModel):
            patient = models.ForeignKey("patients.PatientProfile", ...)
            ...
    """

    clinic = models.ForeignKey(
        "clinics.Clinic",
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_set",
        db_index=True,
    )

    objects = TenantManager()
    unscoped = UnscopedManager()

    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):
    def alive(self):
        return self.filter(is_deleted=False)

    def dead(self):
        return self.filter(is_deleted=True)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)


class SoftDeleteModel(BaseModel):
    """
    Abstract base model adding soft-delete behaviour. Useful for clinical
    and financial records where hard deletion is undesirable (audit trail,
    regulatory compliance).
    """

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, hard=False):
        if hard:
            return super().delete(using=using, keep_parents=keep_parents)
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])
