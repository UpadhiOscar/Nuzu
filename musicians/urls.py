from django.urls import path
from . import views

urlpatterns = [
    path("create-profile/", views.create_profile, name="create_profile"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("browse/", views.browse_musicians, name="browse_musicians"),
    path("<int:pk>/", views.musician_detail, name="musician_detail"),
]