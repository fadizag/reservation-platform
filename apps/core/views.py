from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,render

def landing(request):
    return redirect("core:home") if request.user.is_authenticated else render(request,"core/landing.html")
@login_required
def home(request):
    if request.user.is_admin_role: return redirect("admin_dashboard:overview")
    if request.user.is_driver: return redirect("reservations:driver_dashboard")
    return redirect("reservations:passenger_dashboard")
