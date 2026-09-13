from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.models import TimeStampedModel


class User(AbstractUser):
    class Role(models.TextChoices):
        PASSENGER = "passenger", "Passenger"
        DRIVER = "driver", "Driver"
        ADMIN = "admin", "Administrator"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.PASSENGER)
    phone_number = models.CharField(max_length=32, blank=True)

    @property
    def is_passenger(self):
        return self.role == self.Role.PASSENGER

    @property
    def is_driver(self):
        return self.role == self.Role.DRIVER

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def __str__(self):
        return self.get_full_name() or self.username


class DriverProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="driver_profile")
    vehicle_make = models.CharField(max_length=64, blank=True)
    vehicle_model = models.CharField(max_length=64, blank=True)
    vehicle_plate = models.CharField(max_length=32, blank=True)
    license_number = models.CharField(max_length=64, blank=True)
    is_active = models.BooleanField(default=True)
    rating_average = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)

    def __str__(self):
        return f"Driver: {self.user}"


class PassengerProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="passenger_profile")
    rating_average = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)

    def __str__(self):
        return f"Passenger: {self.user}"
