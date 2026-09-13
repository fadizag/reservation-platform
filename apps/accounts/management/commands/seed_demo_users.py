from django.core.management.base import BaseCommand
from apps.accounts.models import DriverProfile, PassengerProfile, User


class Command(BaseCommand):
    help = "Create or update safe demo passenger and driver accounts."

    PASSWORD = "DemoRide2026!"

    def handle(self, *args, **options):
        passenger, _ = User.objects.get_or_create(username="demo_passenger")
        passenger.role = User.Role.PASSENGER
        passenger.phone_number = "+970590000001"
        passenger.first_name = "Demo"
        passenger.last_name = "Passenger"
        passenger.is_active = True
        passenger.set_password(self.PASSWORD)
        passenger.save()
        PassengerProfile.objects.get_or_create(user=passenger)

        driver, _ = User.objects.get_or_create(username="demo_driver")
        driver.role = User.Role.DRIVER
        driver.phone_number = "+970590000002"
        driver.first_name = "Demo"
        driver.last_name = "Driver"
        driver.is_active = True
        driver.set_password(self.PASSWORD)
        driver.save()
        profile, _ = DriverProfile.objects.get_or_create(user=driver)
        profile.is_active = True
        profile.vehicle_make = "Toyota"
        profile.vehicle_model = "Corolla"
        profile.vehicle_plate = "DEMO-01"
        profile.save()

        self.stdout.write(self.style.SUCCESS("Demo passenger and driver accounts are ready."))
