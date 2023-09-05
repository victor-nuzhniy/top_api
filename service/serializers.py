"""Serializers for 'service' app."""
from rest_framework import serializers

from .models import Check, Printer


class PrinterSerializer(serializers.ModelSerializer):
    """Printer model serializer."""

    class Meta:
        """Class Meta for Printer serializer class."""

        model = Printer
        fields = "__all__"
        read_only_fields = ("id",)


class CheckSerializer(serializers.ModelSerializer):
    """Check model serializer."""

    class Meta:
        """Class Meta for Check serializer class."""

        model = Check
        exclude = "__all__"
        read_only_fields = ("id", "printer_id")
