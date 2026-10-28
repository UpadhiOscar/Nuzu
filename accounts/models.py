from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for the Musician Booking Marketplace.
    """

    email = models.EmailField(unique=True)

    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )

    can_hire = models.BooleanField(default=True)
    can_provide_services = models.BooleanField(default=False)

    def __str__(self):
        return self.username