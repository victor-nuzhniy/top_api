"""Module for testing 'service' tables."""
import pytest

from service.models import Check, Printer
from tests.bases import BaseModelFactory
from tests.service.factories import CheckFactory, PrinterFactory


@pytest.mark.django_db
class TestPrinter:
    """Class for testing Printer model."""

    pytestmark = pytest.mark.django_db

    def test_factory(self) -> None:
        """Test Printer instance creation."""
        BaseModelFactory.check_factory(factory_class=PrinterFactory, model=Printer)

    def test__str__(self) -> None:
        """Test Printer __str__ method."""
        obj: Printer = PrinterFactory()
        expected_result: str = str(obj.name)
        assert expected_result == obj.__str__()


@pytest.mark.django_db
class TestCheck:
    """Class for testing Check model."""

    pytestmark = pytest.mark.django_db

    def test_factory(self) -> None:
        """Test Check instance creation."""
        BaseModelFactory.check_factory(factory_class=CheckFactory, model=Check)

    def test__str__(self) -> None:
        """Test Check __str__ method."""
        obj: Check = CheckFactory()
        expected_result: str = f"Check {obj.printer_id} status {obj.status}"
        assert expected_result == obj.__str__()
