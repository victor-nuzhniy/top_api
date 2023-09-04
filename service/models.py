"""Models for 'service' app."""
from typing import IO

from django.db import models


class Printer(models.Model):
    """Printer model for 'service' app."""

    CHECK_TYPE = [
        ("kitchen", "kitchen"),
        ("client", "client"),
    ]

    name: str = models.CharField(max_length=100, verbose_name="Printer name")
    api_key: str = models.CharField(max_length=150, verbose_name="Printer api key")
    check_type: str = models.CharField(
        max_length=10, choices=CHECK_TYPE, verbose_name="Check type"
    )
    point_id: int = models.IntegerField(verbose_name="Point id")

    def __str__(self) -> str:
        """Represent Printer model."""
        return str(self.name)


class Check(models.Model):
    """Check model for 'service' app."""

    CHECK_TYPE = [
        ("kitchen", "kitchen"),
        ("client", "client"),
    ]

    STATUS = [
        ("new", "new"),
        ("rendered", "rendered"),
        ("printed", "printed"),
    ]

    printer_id: int = models.ForeignKey(
        Printer, on_delete=models.CASCADE, verbose_name="Printer"
    )
    type: str = models.CharField(
        max_length=10, choices=CHECK_TYPE, verbose_name="Check type"
    )
    order: bytes = models.JSONField(verbose_name="Order data")
    status: str = models.CharField(
        max_length=10, choices=STATUS, default="new", verbose_name="Check status"
    )
    pdf_file: IO = models.FileField(
        upload_to=None, blank=True, null=True, verbose_name="PDF file"
    )

    def __str__(self) -> str:
        """Represent Check model."""
        return f"Check {self.printer_id} status {self.status}"
