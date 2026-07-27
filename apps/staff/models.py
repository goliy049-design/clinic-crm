from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.core.exceptions import ValidationError

from core.models import TenantModel


class StaffRole(models.TextChoices):
    DOCTOR = "doctor", "Doctor"
    OPERATOR = "operator", "Operator"
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
    role = models.CharField(
        max_length=20,
        choices=StaffRole.choices,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["user__username"]

    def __str__(self):
        return (
            f"{self.user.username} "
            f"({self.get_role_display()}) @ {self.clinic.name}"
        )


class StaffService(TenantModel):
    """
    Defines which services a staff member can perform.
    Optional duration and price override the defaults defined
    on the Service model.
    """

    staff = models.ForeignKey(
        "staff.StaffProfile",
        on_delete=models.CASCADE,
        related_name="staff_services",
    )

    service = models.ForeignKey(
        "services.ServiceVariant",
        on_delete=models.CASCADE,
        related_name="staff_services",
    )

    duration_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
        help_text="Leave empty to use the service default duration.",
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="Leave empty to use the service default price.",
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = [
            "staff",
            "service",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "staff",
                    "service",
                ],
                name="unique_staff_service",
            ),
        ]

    def __str__(self):
        return (
            f"{self.staff.user.username} - "
            f"{self.service.name}"
        )


class StaffSchedule(TenantModel):
    """
    Defines the working shifts of a staff member.
    One staff member may have multiple shifts per day.
    """

    staff = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name="schedules",
    )

    date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    is_available = models.BooleanField(
        default=True,
    )

    notes = models.CharField(
        max_length=255,
        blank=True,
    )

    class Meta:
        ordering = [
            "date",
            "start_time",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "staff",
                    "date",
                    "start_time",
                ],
                name="unique_staff_shift",
            ),
        ]

    def clean(self):
       if self.start_time and self.end_time:
           if self.start_time >= self.end_time:
               raise ValidationError(
                  "End time must be later than start time."
               )

    def __str__(self):
        return (
            f"{self.staff.user.username} | "
            f"{self.date} "
            f"{self.start_time}-{self.end_time}"
        )    