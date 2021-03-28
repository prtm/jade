from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from . import api_view

router = routers.SimpleRouter()
router.register(r"", api_view.MarketAPIView, basename="market")

urlpatterns = router.urls