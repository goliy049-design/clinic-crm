from django.core.validators import MinValueValidator
from django.db import models

from core.models import TenantModel


class Service(TenantModel):
    """
    A bookable offering at one clinic (e.g. "General Consultation", 30
    min, $50). `clinic` comes from TenantModel — not redeclared here.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Expected length of this service in minutes.",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} @ {self.clinic.name}"
