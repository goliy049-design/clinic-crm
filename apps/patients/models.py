from django.conf import settings
from django.db import models

from core.models import TenantModel


class PatientProfile(TenantModel):
    """
    A patient's record at one clinic. `user` is optional — most patients
    are registered by front-desk staff and never log in; the link can be
    made later if/when patient-portal access is granted. Demographic
    fields live here (not on User) because they need to exist even for
    patients who never get an account.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patient_profile",
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=32, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} @ {self.clinic.name}"
