from django.db import models

from core.models import BaseModel


class Clinic(BaseModel):
    """
    The tenant. Every other piece of business data in the system belongs
    to exactly one Clinic via core.models.TenantModel — Clinic itself
    inherits BaseModel directly (not TenantModel) because it IS the
    tenant boundary, not a tenant-owned record.
    """

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
