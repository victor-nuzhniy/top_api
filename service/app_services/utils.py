"""Utilities for 'service' app."""
import json
from typing import Dict, Optional

from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from service.models import Check, Printer
from service.serializers import CheckSerializer


def get_printers(data: Dict) -> Optional[QuerySet]:
    """Get printers queryset using point_id or raise error if they aren't."""
    point_id: int = data.get("point_id")
    if printers := Printer.objects.filter(point_id=point_id).only("id"):
        return printers
    raise ValidationError({"message": "Point has no printer assigned to."})


def check_order_not_exists(data: Dict) -> None:
    """
    Check whether order does not exists.

    If it exists, raise ValidationError.
    """
    order: bytes = data.get("order")
    if Check.objects.filter(order=order).exists():
        order_data = json.loads(order)
        raise ValidationError(
            {"message": f"Order with id {order_data.get('id')} already exists."}
        )


def perform_check_creation(data: Dict, printers: QuerySet) -> None:
    """
    Perform creation operations with serializer.

    Also add celery task to create pdf file.
    """
    serializer: ModelSerializer = CheckSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    for printer in printers:
        serializer.save(printer_id=printer)
        serializer.instance = None
        # TODO here must be inserted celery task call for pdf file creation


def check_exists(data: Dict) -> Check:
    """
    Get check instance by given data.

    If it's not exist, raise ValidationError. Otherwise return instance.
    """
    check_id: int = data.get("check_id")
    api_key: str = data.get("api_key")
    if instance := Check.objects.filter(
        id=check_id, printer_id__api_key=api_key
    ).first():
        return instance
    raise ValidationError(
        {
            "message": f"Check with id {check_id} created for printer with "
            f"key {api_key} does not exist"
        }
    )


def perform_partial_check_update(instance: Check, data: Dict) -> None:
    """Perform partial update Check model."""
    serializer: ModelSerializer = CheckSerializer(
        instance=instance, data=data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()


def get_check_instance(data: Dict) -> Check:
    """Get Check model instance by pk."""
    pk: int = data.get("pk")
    instance: Check = Check.objects.get(pk=pk)
    if not instance.pdf_file:
        raise ValidationError({"message": "There no check pdf file."})
    return instance
