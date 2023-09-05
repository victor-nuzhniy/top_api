"""Schemas for 'service' app."""
import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

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
