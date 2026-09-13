import os

from django.core.management import call_command
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from .models import DriverProfile, PassengerProfile, User


@receiver(post_save, sender=User)
def ensure_role_profile(sender, instance, created, **kwargs):
    if instance.is_driver:
        DriverProfile.objects.get_or_create(user=instance)
    elif instance.is_passenger:
        PassengerProfile.objects.get_or_create(user=instance)


@receiver(post_migrate)
def seed_demo_accounts_after_migrate(sender, **kwargs):
    if sender.name == "apps.accounts" and os.environ.get("SEED_DEMO_ACCOUNTS") == "1":
        call_command("seed_demo_users", verbosity=0)
