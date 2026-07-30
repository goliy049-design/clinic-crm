from django.core.validators import MinValueValidator
from django.db import models

from core.models import TenantModel


class ServiceCategory(TenantModel):
    """
    Main service categories for a clinic.
    Example:
    - Weight Loss
    - Skin & Rejuvenation
    - Laser
    """

    name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        db_table = "services_serviceline"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Service(TenantModel):
    """
    Main service definition.

    Example:
    Laser
    RF
    Cryolipolysis
    """

    category = models.ForeignKey(
        "services.ServiceCategory",
        on_delete=models.PROTECT,
        related_name="services",
        null=True,
        blank=True,
    )

    name = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True
    )

    duration_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Default duration in minutes.",
        null=True,
        blank=True,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Default service price.",
        null=True,
        blank=True,
    )


    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} @ {self.clinic.name}"

class Room(TenantModel):
    """
    Physical room inside the clinic.
    Equipment can be moved between rooms by the clinic manager.
    """

    name = models.CharField(
        max_length=100,
    )

    description = models.CharField(
        max_length=255,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name



class Equipment(TenantModel):
    """
    Clinic equipment/devices.

    Example:
    - RF Robolux
    - Carbon Laser Device
    - Cryo Machine
    """

    name = models.CharField(
        max_length=255
    )

    brand = models.CharField(
        max_length=150,
        blank=True,
    )

    model = models.CharField(
        max_length=150,
        blank=True,
    )

    room = models.ForeignKey(
    "services.Room",
    on_delete=models.SET_NULL,
    related_name="equipments",
    null=True,
    blank=True,
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ServiceVariant(TenantModel):
    """
    Bookable version of a service.

    Example:
    Service:
        Laser

    Variants:
        Bikini
        Full Face
        Total
    """

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="variants",
    )

    name = models.CharField(
        max_length=255
    )

    duration_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    equipment = models.ManyToManyField(
        Equipment,
        related_name="service_variants",
        blank=True,
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = [
            "service",
            "name",
        ]

    def __str__(self):
        return f"{self.service.name} - {self.name}"