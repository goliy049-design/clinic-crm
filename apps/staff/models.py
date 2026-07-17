from django.conf import settings
from django.db import models

from core.models import TenantModel


class StaffRole(models.TextChoices):
    DOCTOR = "doctor", "Doctor"
    RECEPTIONIST = "receptionist", "Receptionist"
    MANAGER = "manager", "Manager"
    ADMIN = "admin", "Admin"


class StaffProfile(TenantModel):
    """
    Links a User to one Clinic with a role. This — not User — is what
    makes someone "staff": a User with no StaffProfile simply isn't staff
    anywhere. The relationship is deliberately one-to-one for now (one
    person, one staff role, one clinic); if a future requirement needs
    the same person staffing multiple clinics, change `user` to a
    ForeignKey and add a uniqueness constraint on (user, clinic) instead
    of reusing this field as-is.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_profile",
    )
    role = models.CharField(max_length=20, choices=StaffRole.choices)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["user__username"]

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()}) @ {self.clinic.name}"
