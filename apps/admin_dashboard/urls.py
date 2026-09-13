from django.urls import path
from . import views
app_name="admin_dashboard"
urlpatterns=[path("",views.overview,name="overview"),path("disputes/<int:pk>/",views.dispute_review,name="dispute_review"),path("exceptions/<int:pk>/",views.exception_review,name="exception_review")]
