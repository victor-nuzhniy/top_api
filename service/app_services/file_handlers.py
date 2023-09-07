"""File handlers for 'service' app."""
import base64
import json
from typing import Dict

import requests
from django.core.files.base import ContentFile
from django.template.loader import render_to_string

from service.models import Check


def get_pdf_file_name(order_id: int, check_type: str) -> str:
    """Get check pdf file name."""
    return f"{order_id}_{check_type}.pdf"


def create_pdf_data(context: Dict, check_type: str) -> bytes:
    """Create pdf data, using context dict, templates, wkhtmltopdf server."""
    url = "http://127.0.0.1:8001/"
    headers = {
        "Content-Type": "application/json",
    }
    template: str = "client.html" if check_type == "client" else "kitchen.html"
    content = render_to_string(template, context)

    base64_bytes = base64.b64encode(bytes(content, "utf-8"))
    base64_string = base64_bytes.decode("utf-8")

    data = {"contents": base64_string}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response.content


def modify_check_instance(content: bytes, check_id: int, pdf_file: str) -> None:
    """Modify check instance, add created pdf file, change status to 'rendered'."""
    check = Check.objects.get(id=check_id)
    check.pdf_file.save(pdf_file, ContentFile(content))
    check.status = "rendered"
    check.save()


def write_file(context: Dict, check_id: int, check_type: str) -> None:
    """Write pdf file, using check order data, attach it to check model."""
    pdf_file: str = get_pdf_file_name(context.get("id"), check_type)
    content: bytes = create_pdf_data(context, check_type)
    modify_check_instance(content, check_id, pdf_file)
