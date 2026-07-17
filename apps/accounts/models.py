"""
Authentication identity only. This app must never gain a `clinic` FK or
role-specific fields — that's exactly the coupling this architecture is
designed to avoid. Anything tenant-specific or role-specific belongs on
StaffProfile (apps.staff) or PatientProfile (apps.patients) instead, each
linked back to a User via a one-to-one.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom auth user, swapped in via AUTH_USER_MODEL so it can be extended
    later (e.g. MFA, SSO fields) without a disruptive migration. Holds
    nothing about *what* the person is (staff vs patient) or *where*
    they belong (which clinic) — see module docstring.
    """

    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
