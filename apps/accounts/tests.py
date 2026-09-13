import os

from django.core.management import call_command
from django.test import TestCase

from apps.accounts.models import User


class DemoAccountsCommandTests(TestCase):
    def test_seed_demo_users_creates_expected_demo_accounts(self):
        os.environ["DEMO_ACCOUNT_PASSWORD"] = "1234567890"
        try:
            call_command("seed_demo_users")
        finally:
            os.environ.pop("DEMO_ACCOUNT_PASSWORD", None)

        passenger = User.objects.get(username="demo_passenger")
        driver = User.objects.get(username="demo_driver")

        self.assertEqual(passenger.role, User.Role.PASSENGER)
        self.assertEqual(driver.role, User.Role.DRIVER)
        self.assertTrue(passenger.check_password("1234567890"))
        self.assertTrue(driver.check_password("1234567890"))
