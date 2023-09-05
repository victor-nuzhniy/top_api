"""'Service' app urls."""
from django.urls import path

from service.views import CheckPrinterView, CheckView, DownloadCheckView

urlpatterns = [
    path("check/", CheckView.as_view(), name="create_check"),
    path("download/<int:pk>/", DownloadCheckView.as_view(), name="download_check"),
    path("printer/<slug:api_key>/", CheckPrinterView.as_view(), name="rendered_checks"),
]
