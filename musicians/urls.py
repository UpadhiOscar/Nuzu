from django.urls import path
from . import views

urlpatterns = [
    path("create-profile/", views.create_profile, name="create_profile"),
    path("browse/", views.browse_musicians, name="browse_musicians"),

    path("<int:pk>/edit/", views.edit_profile, name="edit_profile"),
    path(
        "<int:pk>/portfolio/manage/",
        views.manage_portfolio,
        name="manage_portfolio",
    ),

    path("<int:pk>/", views.musician_detail, name="musician_detail"),
]