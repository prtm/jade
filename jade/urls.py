# from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from .views import index_view

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("", index_view, name="index"),
    path("market/", include("market.urls")),
]
