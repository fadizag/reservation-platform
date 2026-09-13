import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()

# Preview-only demo accounts. Disabled by default for production safety.
if os.environ.get("SEED_DEMO_USERS") == "1":
    from django.core.management import call_command

    call_command("seed_demo_users")
