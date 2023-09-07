"""Schemas for 'service' app."""
from typing import List

import coreapi
import coreschema
from rest_framework.schemas import AutoSchema


class CheckSchema(AutoSchema):
    """Class for CheckView operation schema."""

    manual_fields: List = []

    def get_manual_fields(self, path: str, method: str) -> List:
        """Get manual_fields for POST and PATCH methods."""
        if method.lower() == "post":
            custom_fields: List = [
                coreapi.Field(
                    name="order",
                    required=True,
                    location="form",
                    schema=coreschema.Object(description="Order data in json format."),
                    description="Order data in json format.",
                ),
                coreapi.Field(
                    name="point_id",
                    required=True,
                    location="form",
                    schema=coreschema.String(description="Point id."),
                ),
            ]
        else:
            custom_fields = [
                coreapi.Field(
                    name="status",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        description="Check status. Choice 'new', 'rendered', 'printed'."
                    ),
                ),
                coreapi.Field(
                    name="api_key",
                    required=True,
                    location="form",
                    schema=coreschema.String(description="Printer api key."),
                ),
                coreapi.Field(
                    name="check_id",
                    required=True,
                    location="form",
                    schema=coreschema.String(description="Check id."),
                ),
            ]
        return self._manual_fields + custom_fields
