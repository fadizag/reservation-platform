from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User,DriverProfile,PassengerProfile
@receiver(post_save,sender=User)
def ensure_role_profile(sender,instance,created,**kwargs):
    if instance.is_driver: DriverProfile.objects.get_or_create(user=instance)
    elif instance.is_passenger: PassengerProfile.objects.get_or_create(user=instance)
