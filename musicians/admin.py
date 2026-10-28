
from django.contrib import admin
from .models import MusicianProfile, MusicianService


@admin.register(MusicianProfile)
class MusicianProfileAdmin(admin.ModelAdmin):
    list_display = (
        "display_name",
        "category",
        "city",
        "state",
        "is_verified",
        "is_available",
    )

    list_filter = (
        "category",
        "state",
        "is_verified",
        "is_available",
    )

    search_fields = (
        "display_name",
        "city",
        "user__username",
        "user__email",
    )


@admin.register(MusicianService)
class MusicianServiceAdmin(admin.ModelAdmin):
    list_display = (
        "service_name",
        "musician",
        "instrument",
        "starting_price",
        "is_active",
    )

    list_filter = (
        "instrument",
        "is_active",
    )

    search_fields = (
        "service_name",
        "musician__display_name",
    )
