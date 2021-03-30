from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from . import api_view
from . import views

router = routers.SimpleRouter()
router.register(r"", api_view.MarketAPIView, basename="market")

urlpatterns = [
    path("download-bhav-data/", views.download_bhav_csv),
]

urlpatterns += router.urls
