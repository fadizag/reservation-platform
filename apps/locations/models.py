from django.db import models
from apps.core.models import TimeStampedModel

class Location(TimeStampedModel):
    label=models.CharField(max_length=255)
    latitude=models.DecimalField(max_digits=9,decimal_places=6)
    longitude=models.DecimalField(max_digits=9,decimal_places=6)
    def __str__(self): return self.label
    @property
    def coordinates(self): return (float(self.latitude),float(self.longitude))

class DriverPosition(TimeStampedModel):
    reservation=models.ForeignKey("reservations.Reservation",on_delete=models.CASCADE,related_name="driver_positions")
    latitude=models.DecimalField(max_digits=9,decimal_places=6)
    longitude=models.DecimalField(max_digits=9,decimal_places=6)
    recorded_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=["-recorded_at"]
