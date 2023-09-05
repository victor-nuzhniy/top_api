"""Class and function views of 'service' app."""
import json
from typing import Any

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from service.models import Check, Printer
from service.schemas import create_check_schema
from service.serializers import CheckSerializer


class CheckCreateView(APIView):
    """Class view with only POST method for creating check."""

    schema: AutoSchema = create_check_schema

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
            serializer.save(printer_id=printer.id)
            serializer.instance = None
            # TODO here must be inserted celery task call for pdf file creation
        return Response({"message": "Checks were successfully created."})
