from django.db import models  # noqa: F401

from core.models import TenantModel  # noqa: F401

# Models for the Integrations app. Not created yet — this is an architecture-only
# pass. When added, every model here must inherit TenantModel, e.g.:
#
# class Example(TenantModel):
#     ...
