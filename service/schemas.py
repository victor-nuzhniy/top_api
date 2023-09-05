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
                    name="type",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        description="Check type. Choice from 'kitchen' and 'client'."
                    ),
                ),
                coreapi.Field(
                    name="order",
                    required=True,
                    location="form",
                    schema=coreschema.String(description="Order data."),
                    description="Order data.",
                ),
                coreapi.Field(
                    name="status",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        description="Check status. Choice from "
                        "'new', 'rendered', 'printed'."
                    ),
                ),
                coreapi.Field(
                    name="point_id",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        description="Check status. Choice from 'new',"
                        " 'rendered', 'printed'."
                    ),
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


create_check_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            name="type",
            required=True,
            location="form",
            schema=coreschema.String(
                description="Check type. Choice from 'kitchen' and 'client'."
            ),
        ),
        coreapi.Field(
            name="order",
            required=True,
            location="form",
            schema=coreschema.String(description="Order data."),
            description="Order data.",
        ),
        coreapi.Field(
            name="status",
            required=True,
            location="form",
            schema=coreschema.String(
                description="Check status. Choice from 'new', 'rendered', 'printed'."
            ),
        ),
        coreapi.Field(
            name="point_id",
            required=True,
            location="form",
            schema=coreschema.String(
                description="Check status. Choice from 'new', 'rendered', 'printed'."
            ),
        ),
    ],
)
