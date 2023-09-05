"""Admin site configurations for 'service' app."""
from django.contrib import admin

from .models import Check, Printer


class CheckAdmin(admin.ModelAdmin):
    """Check model admin site settings."""

    list_display = ("id", "printer_id", "type", "status")
    list_display_links = ("id", "printer_id", "type")


class PrinterAdmin(admin.ModelAdmin):
    """Printer model admin site settings."""

    list_display = ("id", "name", "api_key", "check_type", "point_id")
    list_display_links = ("id", "name", "api_key")


admin.site.register(Check, CheckAdmin)
admin.site.register(Printer, PrinterAdmin)
