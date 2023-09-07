"""Factories for testing 'service' app."""
from typing import Dict

import factory

from service.models import Check, Printer
from tests.bases import BaseModelFactory


class PrinterFactory(BaseModelFactory):
    """Factory for testing Printer model."""

    class Meta:
        """Class Meta for PrinterFactory."""

        model = Printer
        exclude = ("check_set",)

    name: str = factory.Faker("pystr", min_chars=1, max_chars=100)
    api_key: str = factory.Faker("pystr", min_chars=10, max_chars=150)
    check_type: str = factory.Faker("random_element", elements=("kitchen", "client"))
    point_id: str = factory.Faker("pyint", min_value=1)
    check_set = factory.RelatedFactoryList(
        factory="tests.service.factories.CheckFactory",
        factory_related_name="check_set",
        size=0,
    )


class CheckFactory(BaseModelFactory):
    """Factory for testing Check model."""

    class Meta:
        """Class Meta for CheckFactory."""

        model = Check
        django_get_or_create = ("printer_id",)

    printer_id: int = factory.SubFactory(PrinterFactory)
    type: str = factory.Faker("random_element", elements=("kitchen", "client"))
    order: Dict = factory.Faker("pydict")
    status: str = factory.Faker(
        "random_element", elements=("new", "rendered", "printed")
    )
    pdf_file = factory.django.FileField()
