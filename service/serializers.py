"""Serializers for 'service' app."""
from rest_framework import serializers

from .models import Check


class CheckSerializer(serializers.ModelSerializer):
    """Check model serializer."""

    class Meta:
        """Class Meta for Check serializer class."""

        model = Check
        fields = "__all__"
        read_only_fields = ("id", "printer_id")
