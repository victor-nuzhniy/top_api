"""Utilities for 'service' app."""
import base64
import json
from typing import Dict, Optional

import requests
from django.core.files.base import ContentFile
from django.db.models import QuerySet
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.serializers import ModelSerializer

from service.app_services.exceptions import CustomValidationError
from service.models import Check, Printer
from service.serializers import CheckSerializer


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
        # TODO here must be inserted celery task call for pdf file creation
        write_file(data.get("order"), serializer.instance.pk, printer.check_type)
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


def get_pdf_file_name(order_id: int, check_type: str) -> str:
    """Get check pdf file name."""
    return f"{order_id}_{check_type}.pdf"


def create_pdf_data(context: Dict, check_type: str) -> bytes:
    """Create pdf data, using context dict, templates, wkhtmltopdf server."""
    url = "http://127.0.0.1:8001/"
    headers = {
        "Content-Type": "application/json",
    }
    template: str = "client.html" if check_type == "client" else "kitchen.html"
    content = render_to_string(template, context)

    base64_bytes = base64.b64encode(bytes(content, "utf-8"))
    base64_string = base64_bytes.decode("utf-8")

    data = {"contents": base64_string}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response.content


def modify_check_instance(content: bytes, check_id: int, pdf_file: str) -> None:
    """Modify check instance, add created pdf file, change status to 'rendered'."""
    check = Check.objects.get(id=check_id)
    check.pdf_file.save(pdf_file, ContentFile(content))
    check.status = "rendered"
    check.save()


def write_file(context: Dict, check_id: int, check_type: str) -> None:
    """Write pdf file, using check order data, attach it to check model."""
    pdf_file: str = get_pdf_file_name(context.get("id"), check_type)
    content: bytes = create_pdf_data(context, check_type)
    modify_check_instance(content, check_id, pdf_file)
