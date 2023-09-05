"""Swagger schemas for 'service' api."""
from drf_yasg import openapi

swagger_check_create_schema = openapi.Schema(
    title="Create check",
    type=openapi.TYPE_OBJECT,
    properties={
        "type": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Check type. Choice from 'kitchen' and 'client'.",
            example="kitchen",
        ),
        "order": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description="Order in json format",
            properties={},
            example='{"id": 1, "soap": {"price": 100, "quantity": 2}}',
        ),
        "status": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Check status. Choice from " "'new', 'rendered', 'printed'.",
            example="new",
        ),
        "point_id": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="Point id", example=1
        ),
    },
)


swagger_check_create_responses = {
    200: "Check was successfully created.",
    400: "Validation errors.",
    404: "Point has no printer assigned to.",
    409: "Order with id already exists.",
}


swagger_check_patch_schema = openapi.Schema(
    title="Patch check",
    type=openapi.TYPE_OBJECT,
    properties={
        "status": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Check status. Choice from " "'new', 'rendered', 'printed'.",
            example="printed",
        ),
        "api_key": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Printer api key.",
            example=1,
        ),
        "check_id": openapi.Schema(
            type=openapi.TYPE_INTEGER,
            default="Check id",
            example=1,
        ),
    },
)


swagger_check_patch_responses = {
    200: "Successfully changed check status",
    400: "Validation errors.",
    404: "Check with id created for printer with key does not exist",
}


swagger_download_responses = {
    200: "Successfully download pdf file.",
    404: "There is no check pdf file.",
}
