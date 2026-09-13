from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render
from apps.reservations.models import Reservation
from apps.disputes.models import Dispute

def is_admin(user): return user.is_authenticated and user.is_admin_role
@login_required
@user_passes_test(is_admin,login_url="core:home")
def overview(request):
    s=Reservation.Status; qs=Reservation.objects.all()
    counts={"total":qs.count(),"active":qs.exclude(status__in=[s.COMPLETED,s.CANCELLED,s.PASSENGER_NO_SHOW,s.DRIVER_NO_SHOW]).count(),"pending":qs.filter(status=s.PENDING).count(),"completed":qs.filter(status=s.COMPLETED).count(),"cancelled":qs.filter(status=s.CANCELLED).count(),"disputed":qs.filter(status=s.DISPUTED).count()}
    return render(request,"admin_dashboard/overview.html",{"counts":counts,"open_disputes":Dispute.objects.filter(status__in=["open","under_review"]),"recent_reservations":qs[:10]})
@login_required
@user_passes_test(is_admin,login_url="core:home")
def dispute_review(request,pk):
    return render(request,"admin_dashboard/dispute_review.html",{"dispute":Dispute.objects.get(pk=pk)})
@login_required
@user_passes_test(is_admin,login_url="core:home")
def exception_review(request,pk):
    from apps.reservations.models import CancellationExceptionRequest
    return render(request,"admin_dashboard/exception_review.html",{"exception_request":CancellationExceptionRequest.objects.get(pk=pk)})
