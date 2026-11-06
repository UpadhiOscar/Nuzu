
from django.contrib import admin
from django.urls import path, include

from config.views import home


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("accounts/", include("accounts.urls")),
    path("musicians/", include("musicians.urls")),
]
