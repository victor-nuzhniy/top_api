"""Class and function views of 'service' app."""
from typing import Any, Optional

from django.db.models import QuerySet
from django.http import FileResponse
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from service.app_services.utils import (
    check_exists,
    check_order_not_exists,
    get_check_instance,
    get_printers,
    perform_check_creation,
    perform_partial_check_update,
)
from service.models import Check
from service.schemas import CheckSchema
from service.serializers import CheckSerializer


class CheckView(APIView):
    """Class view with only POST method for creating check."""

    schema: AutoSchema = CheckSchema()

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Handle post request."""
        printers: Optional[QuerySet] = get_printers(request.data)
        check_order_not_exists(request.data)
        perform_check_creation(request.data, printers=printers)
        return Response({"message": "Checks were successfully created."})

    def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Change Check status field."""
        instance = check_exists(request.data)
        perform_partial_check_update(instance, request.data)
        return Response({"message": "Successfully changed check status"})


class CheckPrinterView(generics.ListAPIView):
    """Class view with GET method to retrieve rendered and not printed checks."""

    serializer_class: ModelSerializer = CheckSerializer
    schema: AutoSchema = AutoSchema()
    queryset: QuerySet = Check.objects.all()

    def get_queryset(self) -> QuerySet:
        """Get view queryset - rendered and not printed checks for the printer."""
        queryset: QuerySet = super().get_queryset()
        api_key: str = self.kwargs.get("api_key")
        return queryset.filter(printer_id__api_key=api_key).filter(status="rendered")


class DownloadCheckView(APIView):
    """Class view with GET method to download single check pdf file."""

    schema: AutoSchema = AutoSchema()

    def get(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> FileResponse | Response:
        """Download file with GET request."""
        instance: Check = get_check_instance(self.kwargs)
        file = instance.pdf_file.open()
        response = FileResponse(file, content_type="application/pdf")
        response["Content-Length"] = instance.pdf_file.size
        response[
            "Content-Disposition"
        ] = f'attachment; filename="{instance.pdf_file.name}"'
        return response
