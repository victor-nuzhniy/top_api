"""Apps module for 'service' app."""
from django.apps import AppConfig


class ServiceConfig(AppConfig):
    """'Service' app configs."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "service"
