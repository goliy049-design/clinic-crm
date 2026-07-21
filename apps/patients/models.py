from django.conf import settings
from django.db import models

from core.models import TenantModel


class PatientProfile(TenantModel):
    """
    Patient record inside a clinic.
    """

    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patient_profile",
    )

    first_name = models.CharField(
        max_length=150
    )

    last_name = models.CharField(
        max_length=150
    )

    phone_number = models.CharField(
        max_length=32,
        blank=True,
    )

    national_code = models.CharField(
        max_length=10,
        blank=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    emergency_contact = models.CharField(
        max_length=150,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = [
            "last_name",
            "first_name",
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} @ {self.clinic.name}"