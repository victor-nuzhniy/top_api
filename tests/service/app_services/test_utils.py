"""Module for testing service.app_services.utils."""
from typing import Dict, List
from unittest.mock import MagicMock, patch

import pytest
from django.db.models import QuerySet
from faker import Faker
from rest_framework.exceptions import ValidationError

from service.app_services.exceptions import CustomValidationError
from service.app_services.file_handlers import write_file
from service.app_services.utils import (
    check_exists,
    check_order_not_exists,
    get_check_instance,
    get_printers,
    perform_check_creation,
    perform_partial_check_update,
)
from service.models import Check, Printer
from tests.service.factories import CheckFactory, PrinterFactory


@pytest.mark.django_db
class TestGetPrinters:
    """Class for testing get_printers function."""

    pytestmark = pytest.mark.django_db

    def test_get_printers(self, faker: Faker) -> None:
        """Test get_printers."""
        point_id: int = faker.random_int(min=10000, max=99999)
        printers: List[Printer] = PrinterFactory.create_batch(size=3, point_id=point_id)
        data: Dict = faker.pydict(
            allowed_types=["int", "str"], value_types=["int", "str"]
        )
        data["point_id"] = point_id
        expected_result: QuerySet = get_printers(data)
        for i, printer in enumerate(printers):
            assert printer.pk == expected_result[i].pk
            assert printer.check_type == expected_result[i].check_type

    def test_get_printers_empty(self, faker: Faker) -> None:
        """Test get_printers empty output."""
        point_id: int = faker.random_int(min=10000, max=99999)
        data: Dict = faker.pydict(
            allowed_types=["int", "str"], value_types=["int", "str"]
        )
        data["point_id"] = point_id
        try:
            get_printers(data)
            assert False
        except CustomValidationError:
            assert True


@pytest.mark.django_db
class TestCheckOrderNotExists:
    """Class for testing check_order_not_exists function."""

    pytestmark = pytest.mark.django_db

    def test_check_order_not_exists(self, faker: Faker) -> None:
        """Test check_order_not_exists."""
        check: Check = CheckFactory()
        data: Dict = faker.pydict(
            allowed_types=["int", "str"], value_types=["int", "str"]
        )
        data["order"] = check.order
        try:
            check_order_not_exists(data)
            assert False
        except CustomValidationError:
            assert True

    def test_check_order_not_exists_empty(self, faker: Faker) -> None:
        """Test check_order_not_exists."""
        data: Dict = faker.pydict(
            allowed_types=["int", "str"], value_types=["int", "str"]
        )
        data["order"] = faker.pystr(min_chars=4, max_chars=30)
        assert not check_order_not_exists(data)


@pytest.mark.django_db
class TestPerformCheckCreation:
    """Class for testing perform_check_creation function."""

    pytestmark = pytest.mark.django_db

    @patch("service.tasks.perform_file_writing.delay")
    def test_perform_check_creation(self, get_mock: MagicMock, faker: Faker) -> None:
        """Test perform_check_creation."""
        point_id: int = faker.random_int(min=10000, max=99999)
        PrinterFactory(check_type="kitchen", point_id=point_id)
        PrinterFactory(check_type="client", point_id=point_id)
        printers: QuerySet = Printer.objects.filter(point_id=point_id)
        get_mock.side_effect = write_file
        data: Dict = {
            "order": {
                "id": faker.random_int(min=10),
                "date": faker.date(),
                "point": faker.pydict(
                    allowed_types=["int", "str"], value_types=["int", "str"]
                ),
                "products": faker.pylist(
                    allowed_types=["int", "str"], value_types=["int", "str"]
                ),
                "total": faker.random_int(),
            },
            "point_id": point_id,
        }
        perform_check_creation(data, printers)
        for printer in printers:
            check: Check = Check.objects.get(printer_id=printer)
            assert check.type == printer.check_type
            assert check.order == data.get("order")
            assert check.status == "rendered"
            assert (
                check.pdf_file.name
                == f"pdf/{data.get('order').get('id')}_{printer.check_type}.pdf"
            )

    def test_perform_check_creation_serializer_err(self, faker: Faker) -> None:
        """Test perform_check_creation. Catch serializer error."""
        point_id: int = faker.random_int(min=10000, max=99999)
        PrinterFactory.create_batch(size=2, point_id=point_id)
        printers: QuerySet = Printer.objects.filter(point_id=point_id)
        data: Dict = {"point_id": point_id}
        try:
            perform_check_creation(data, printers)
            assert False
        except ValidationError:
            assert True


@pytest.mark.django_db
class TestCheckExists:
    """Class for testing check_exists function."""

    pytestmark = pytest.mark.django_db

    def test_check_exists(self) -> None:
        """Test check_exists function."""
        check: Check = CheckFactory()
        data: Dict = {
            "check_id": check.pk,
            "api_key": check.printer_id.api_key,
        }
        expected_result: Check = check_exists(data)
        assert check == expected_result

    def test_check_exists_not_exists(self, faker: Faker) -> None:
        """Test check_exists function. Check does not exist."""
        data: Dict = {
            "check_id": faker.random_int(),
            "api_key": faker.pystr(),
        }
        try:
            check_exists(data)
            assert False
        except CustomValidationError:
            assert True


@pytest.mark.django_db
class TestPerformPartialCheckUpdate:
    """Class for testing perform_partial_check_update function."""

    pytestmark = pytest.mark.django_db

    def test_perform_partial_check_update(self, faker: Faker) -> None:
        """Test perform_partial_check_update."""
        check: Check = CheckFactory(status="new")
        data: Dict = {"status": "rendered"}
        perform_partial_check_update(check, data)
        assert check.status == "rendered"

    def test_perform_partial_check_update_validationerror(self) -> None:
        """Test perform_partial_check_update. Check ValidationError raising."""
        check: Check = CheckFactory(status="new")
        data: Dict = {"status": "ren"}
        try:
            perform_partial_check_update(check, data)
            assert False
        except ValidationError:
            assert True


@pytest.mark.django_db
class TestGetCheckInstance:
    """Class for testing get_check_instance function."""

    pytestmark = pytest.mark.django_db

    def test_get_check_instance(self) -> None:
        """Test get_check_instance function."""
        check: Check = CheckFactory()
        data: Dict = {"pk": check.pk}
        expected_result: Check = get_check_instance(data)
        assert check == expected_result

    def test_get_check_instance_not_file(self) -> None:
        """Test get_check_instance function. No pdf_file."""
        check: Check = CheckFactory(pdf_file=None)
        data: Dict = {"pk": check.pk}
        try:
            get_check_instance(data)
            assert False
        except CustomValidationError:
            assert True
