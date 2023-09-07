"""Module for celery tasks for 'service' app."""
from __future__ import absolute_import, unicode_literals

from typing import Dict

from celery import shared_task

from service.app_services.file_handlers import write_file


@shared_task()
def perform_file_writing(context: Dict, check_id: int, check_type: str) -> None:
    """Perform write file operation."""
    write_file(context, check_id, check_type)
