"""Utilities for 'service' app."""
from typing import Dict, Optional

from django.db.models import QuerySet
from rest_framework import status
from rest_framework.serializers import ModelSerializer

from service.app_services.exceptions import CustomValidationError
from service.models import Check, Printer
from service.serializers import CheckSerializer
from service.tasks import perform_file_writing


def get_printers(data: Dict) -> Optional[QuerySet]:
    """Get printers queryset using point_id or raise error if they aren't."""
    point_id: int = data.get("point_id")
    if printers := Printer.objects.filter(point_id=point_id).only("check_type"):
        return printers
    raise CustomValidationError(
        detail="Point has no printer assigned to.",
        field="message",
        status_code=status.HTTP_404_NOT_FOUND,
    )


def check_order_not_exists(data: Dict) -> None:
    """
    Check whether order does not exists.

    If it exists, raise ValidationError.
    """
    order: Dict = data.get("order")
    if Check.objects.filter(order=order).exists():
        raise CustomValidationError(
            detail=f"Order with id {order.get('id')} already exists.",
            field="message",
            status_code=status.HTTP_409_CONFLICT,
        )


def perform_check_creation(data: Dict, printers: QuerySet) -> None:
    """
    Perform creation operations with serializer.

    Also add celery task to create pdf file.
    """
    serializer: ModelSerializer = CheckSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    for printer in printers:
        serializer.save(printer_id=printer, type=printer.check_type)
        perform_file_writing.delay(
            data.get("order"), serializer.instance.pk, printer.check_type
        )
        serializer.instance = None


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
    raise CustomValidationError(
        detail=f"Check with id {check_id} created for printer with "
        f"key {api_key} does not exist",
        field="message",
        status_code=status.HTTP_404_NOT_FOUND,
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
        raise CustomValidationError(
            detail="There is no check pdf file.",
            field="message",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return instance
