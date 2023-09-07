"""Module for testing 'servise' app views."""
import json
from typing import Dict, List
from unittest.mock import MagicMock, patch

import pytest
from django.test import Client
from django.urls import reverse
from faker import Faker

from service.app_services.file_handlers import write_file
from service.models import Check, Printer
from tests.service.factories import CheckFactory, PrinterFactory


@pytest.mark.django_db
class TestCheckView:
    """Class for testing CheckView functionality."""

    pytestmark = pytest.mark.django_db

    @patch("service.tasks.perform_file_writing")
    def test_post_method(
        self, get_mock: MagicMock, faker: Faker, client: Client
    ) -> None:
        """Test CheckView post method."""
        point_id: int = faker.random_int(min=10000, max=99999)
        printers: List[Printer] = [
            PrinterFactory(point_id=point_id, check_type="kitchen"),
            PrinterFactory(point_id=point_id, check_type="client"),
        ]
        get_mock.side_effect = write_file
        data: Dict = {
            "order": json.dumps(
                {
                    "id": 78563,
                    "date": "2012/12/12",
                    "point": {
                        "id": 1,
                        "name": "Spanish pilot",
                    },
                    "products": [
                        {
                            "id": 1,
                            "name": "Soap",
                            "code": "1452984",
                            "quantity": 2,
                            "price": 100,
                            "sum": 200,
                        },
                        {
                            "id": 2,
                            "name": "Soap",
                            "code": "1452984",
                            "quantity": 2,
                            "price": 100,
                            "sum": 200,
                        },
                    ],
                    "total": 200,
                }
            ),
            "point_id": point_id,
        }
        url: str = reverse("create_check")
        response = client.post(url, data=data)
        assert response.status_code == 200
        assert response.json().get("message") == "Checks were successfully created."
        for printer in printers:
            check: Check = Check.objects.filter(printer_id=printer).last()
            assert check.type == printer.check_type
            assert check.status == "new"

    def test_patch_method(self, faker: Faker, client: Client) -> None:
        """Test CheckView patch method."""
        printer: Printer = PrinterFactory()
        check: Check = CheckFactory(printer_id=printer, status="new")
        data: Dict = {
            "status": "printed",
            "api_key": printer.api_key,
            "check_id": check.pk,
        }
        url: str = reverse("create_check")
        headers: Dict = {"Content-Type": "application/json"}
        response = client.patch(url, data=json.dumps(data), headers=headers)
        expected_check: Check = Check.objects.get(id=check.id)
        assert response.status_code == 200
        assert response.json().get("message") == "Successfully changed check status"
        assert expected_check.status == "printed"


@pytest.mark.django_db
class TestCheckPrinterView:
    """Class for testing CheckPrinterView functionality."""

    pytestmark = pytest.mark.django_db

    def test_check_printer_get_method(self, faker: Faker, client: Client) -> None:
        """Test CheckPrinterView get method."""
        printer: Printer = PrinterFactory()
        checks: List = []
        for _ in range(3):
            checks.append(
                Check.objects.create(
                    printer_id=printer,
                    type=printer.check_type,
                    order=faker.pydict(
                        value_types=["int", "str", "dict", "list"],
                        allowed_types=["int", "str", "dict", "list"],
                    ),
                    status="rendered",
                )
            )
        url: str = reverse("rendered_checks", kwargs={"api_key": printer.api_key})
        response = client.get(url)
        result = response.json()
        assert response.status_code == 200
        for i, check in enumerate(checks):
            assert check.pk == result[i].get("id")
            assert check.status == result[i].get("status")
            assert check.type == result[i].get("type")


@pytest.mark.django_db
class TestDownloadCheckView:
    """Class for testing DownloadCheckView functionality."""

    pytestmark = pytest.mark.django_db

    def test_get_method(self, client: Client, faker: Faker) -> None:
        """Test DownloadCheckView get method."""
        check: Check = CheckFactory()
        url: str = reverse("download_check", kwargs={"pk": check.pk})
        response = client.get(url)
        assert response.status_code == 200
        assert (
            response.get("Content-Disposition")
            == f'attachment; filename="{check.pdf_file}"'
        )
