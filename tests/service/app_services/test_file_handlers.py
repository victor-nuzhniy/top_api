"""Module for testing service.app_services.file_handlers functionality."""
from faker import Faker

from service.app_services.file_handlers import get_pdf_file_name


class TestGetPdfFileName:
    """Class for testing get_pdf_file_name function."""

    def test_get_pdf_file_name(self, faker: Faker) -> None:
        """Test get_pdf_file_name function."""
        order_id: int = faker.random_int(min=1)
        check_type: str = faker.pystr(min_chars=1, max_chars=10)
        expected_result: str = get_pdf_file_name(order_id, check_type)
        assert expected_result == f"{order_id}_{check_type}.pdf"
