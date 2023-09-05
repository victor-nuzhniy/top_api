"""'Service' app urls."""
from django.urls import path

from service.views import CheckCreateView

urlpatterns = [
    path("check/", CheckCreateView.as_view(), name="create_check"),
]
