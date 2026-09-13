from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("reservations/", include("apps.reservations.urls")),
    path("notifications/", include("apps.notifications.urls")),
    path("dashboard/", include("apps.admin_dashboard.urls")),
]
