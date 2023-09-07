"""Pytest fixtures for 'top_api' project."""
import random

import pytest
from django.core.management import call_command
from faker import Faker

from tests.service.factories import CheckFactory, PrinterFactory


@pytest.fixture(scope="function", autouse=True)
def faker_seed() -> None:
    """Generate random seed for Faker instance."""
    return random.seed(version=3)


@pytest.fixture()
def create_printer_fixture(faker: Faker) -> None:
    """
    Create printer_fixture.json.

    This fixture is used for creating 'printer_fixtures.json' file for creating initial
    data for test database. To invoke this fixture you have to set scope='function',
    autouse=True as fixture decorator argument and once run test with one test function.
    The 'printer_fixtures.json' file will be created in tests folder. It may be need to
    convert 'printer_fixtures.json' code to 'utf-8', use 'NotePad' for that. There is a
    need to comment custom django_db_setup fixture below.
    """
    for _ in range(20):
        PrinterFactory(
            name=f"{faker.country()}_{faker.city()}",
            api_key=str(faker.pyint(min_value=1000)),
        )
    call_command("dumpdata", exclude=["contenttypes"], output="printer_fixture.json")


@pytest.fixture()
def products_preparation_for_view_testing(faker: Faker) -> None:
    """
    Create data.json fixture.

    This fixture is used for creating 'printer_fixtures.json' file for creating initial
    data for test database. To invoke this fixture you have to set scope='function',
    autouse=True as fixture decorator argument and once run test with one test function.
    The 'printer_fixtures.json' file will be created in tests folder. It may be need to
    convert 'printer_fixtures.json' code to 'utf-8', use 'NotePad' for that. There is a
    need to comment custom django_db_setup fixture below.
    """
    PrinterFactory.create_batch(size=5)
    CheckFactory.create_batch(size=10)
    call_command("dumpdata", exclude=["contenttypes"], output="data.json")


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Use data.json fixture.

    'data.json' file have to be created using
    product_preparation_for_view_testing fixture
    """
    with django_db_blocker.unblock():
        call_command("loaddata", "data.json")
