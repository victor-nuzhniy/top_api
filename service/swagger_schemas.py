"""Swagger schemas for 'service' api."""
from drf_yasg import openapi

swagger_check_create_schema = openapi.Schema(
    title="Create check",
    type=openapi.TYPE_OBJECT,
    properties={
        "order": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description="Order in json format",
            properties={
                "id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="Order id", example=1
                ),
                "date": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Order date.",
                    example="2012/12/12",
                ),
                "point": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Point id",
                            example=1,
                        ),
                        "name": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Point name",
                            example="Spanish pilot",
                        ),
                    },
                ),
                "products": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="Order products",
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description="Order product",
                        properties={
                            "id": openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description="Product number in order",
                                example=1,
                            ),
                            "name": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Product name",
                                example="Soap",
                            ),
                            "code": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Product code",
                                example="1452984",
                            ),
                            "quantity": openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description="Product quantity",
                                example=2,
                            ),
                            "price": openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description="Product price",
                                example=100,
                            ),
                            "sum": openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description="Product sum",
                                example=200,
                            ),
                        },
                    ),
                ),
                "total": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Order sum",
                    example=200,
                ),
            },
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
