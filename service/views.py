"""Class and function views of 'service' app."""
import json
from typing import Any

from django.db.models import QuerySet
from django.http import FileResponse
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from service.models import Check, Printer
from service.schemas import CheckSchema
from service.serializers import CheckSerializer


class CheckView(APIView):
    """Class view with only POST method for creating check."""

    schema: AutoSchema = CheckSchema()

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Handle post request."""
        serializer: Serializer = CheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        point_id: int = request.data.get("point_id")
        if not (printers := Printer.objects.filter(point_id=point_id).only("id")):
            return Response(
                {"message": "Point has no printer assigned to."},
                status=status.HTTP_404_NOT_FOUND,
            )
        order: bytes = request.data.get("order")
        if Check.objects.filter(order=order).exists():
            order_data = json.loads(order)
            return Response(
                {"message": f"Order with id {order_data.get('id')} already exists."},
                status=status.HTTP_409_CONFLICT,
            )
        for printer in printers:
            serializer.save(printer_id=printer)
            serializer.instance = None
            # TODO here must be inserted celery task call for pdf file creation
        return Response({"message": "Checks were successfully created."})

    def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Change Check status field."""
        check_id: int = request.data.get("check_id")
        api_key: str = request.data.get("api_key")
        check_status: str = request.data.get("status")
        if instance := Check.objects.filter(
            id=check_id, printer_id__api_key=api_key
        ).first():
            serializer: Serializer = CheckSerializer(
                instance=instance, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"message": f"Successfully changed check status on {check_status}"}
            )
        return Response(
            {
                "message": f"Check with id {check_id} created for printer with "
                f"key {api_key} does not exist"
            }
        )


class CheckPrinterView(generics.ListAPIView):
    """Class view with GET method to retrieve rendered and not printed checks."""

    serializer_class: Serializer = CheckSerializer
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
        pk: int = self.kwargs.get("pk")
        instance: Check = Check.objects.get(pk=pk)
        if not instance.pdf_file:
            return Response(
                {"message": "There no check pdf file."},
                status=status.HTTP_404_NOT_FOUND,
            )
        file = instance.pdf_file.open()
        response = FileResponse(file, content_type="application/pdf")
        response["Content-Length"] = instance.pdf_file.size
        response[
            "Content-Disposition"
        ] = f'attachment; filename="{instance.pdf_file.name}"'
        return response
