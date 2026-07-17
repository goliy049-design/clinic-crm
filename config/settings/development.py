from .base import *  # noqa: F401, F403

DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += []  # room for dev-only tools, e.g. django-debug-toolbar

CORS_ALLOW_ALL_ORIGINS = True
