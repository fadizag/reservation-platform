from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from apps.reservations.forms import ReservationCreateForm, DelayRequestForm, CancellationForm, DisputeForm
from apps.reservations.models import Reservation, DelayRequest
from apps.reservations.services import state_machine, delay, cancellation, no_show


def _can_view(r, u):
    return u in (r.passenger, r.driver) or u.is_admin_role


@login_required
def reservation_index(request):
    """Stable landing route for the reservations section."""
    return redirect("core:home")


@login_required
def passenger_dashboard(request):
    if not request.user.is_passenger:
        return redirect("core:home")
    qs = request.user.reservations_as_passenger.all()
    return render(
        request,
        "reservations/passenger_dashboard.html",
        {
            "upcoming": qs.exclude(status__in=[Reservation.Status.COMPLETED, Reservation.Status.CANCELLED]),
            "history": qs.filter(status__in=[Reservation.Status.COMPLETED, Reservation.Status.CANCELLED])[:20],
        },
    )


@login_required
def driver_dashboard(request):
    if not request.user.is_driver:
        return redirect("core:home")
    return render(
        request,
        "reservations/driver_dashboard.html",
        {
            "available": Reservation.objects.filter(status=Reservation.Status.PENDING),
            "my_rides": request.user.reservations_as_driver.exclude(
                status__in=[Reservation.Status.COMPLETED, Reservation.Status.CANCELLED]
            ),
            "history": request.user.reservations_as_driver.filter(status=Reservation.Status.COMPLETED)[:20],
        },
    )


@login_required
def reservation_create(request):
    if not request.user.is_passenger:
        raise PermissionDenied
    form = ReservationCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        r = form.save(request.user)
        messages.success(request, "تم إنشاء الحجز بنجاح.")
        return redirect("reservations:detail", r.pk)
    return render(request, "reservations/reservation_form.html", {"form": form})


@login_required
def reservation_detail(request, pk):
    r = get_object_or_404(Reservation, pk=pk)
    if not _can_view(r, request.user):
        raise PermissionDenied
    return render(
        request,
        "reservations/reservation_detail.html",
        {
            "reservation": r,
            "events": r.events.all(),
            "delay_form": DelayRequestForm(),
            "cancel_form": CancellationForm(),
            "dispute_form": DisputeForm(),
            "passenger_no_show_check": no_show.check_passenger_no_show_eligible(r) if request.user == r.driver else None,
            "driver_no_show_check": no_show.check_driver_no_show_eligible(r) if request.user == r.passenger else None,
        },
    )


@login_required
def reservation_accept(request, pk):
    r = get_object_or_404(Reservation, pk=pk, status=Reservation.Status.PENDING)
    if not request.user.is_driver:
        raise PermissionDenied
    r.driver = request.user
    r.save(update_fields=["driver"])
    state_machine.transition(r, Reservation.Status.CONFIRMED, actor=request.user, reason="Driver accepted")
    return redirect("reservations:detail", pk)


def _transition(request, pk, to, role):
    r = get_object_or_404(Reservation, pk=pk, **role)
    state_machine.transition(r, to, actor=request.user, reason="Status updated")
    return redirect("reservations:detail", pk)


@login_required
def driver_depart(request, pk):
    return _transition(request, pk, Reservation.Status.DRIVER_ON_THE_WAY, {"driver": request.user})


@login_required
def driver_arrive(request, pk):
    r = get_object_or_404(Reservation, pk=pk, driver=request.user)
    state_machine.transition(r, Reservation.Status.DRIVER_ARRIVED, actor=request.user, reason="Driver arrived")
    r.waiting_deadline = timezone.now() + timezone.timedelta(minutes=10)
    r.save(update_fields=["waiting_deadline"])
    state_machine.transition(r, Reservation.Status.WAITING, actor=request.user, reason="Waiting started")
    return redirect("reservations:detail", pk)


@login_required
def passenger_checkin(request, pk):
    return _transition(request, pk, Reservation.Status.IN_PROGRESS, {"passenger": request.user})


@login_required
def reservation_complete(request, pk):
    return _transition(request, pk, Reservation.Status.COMPLETED, {"driver": request.user})


@login_required
def reservation_cancel(request, pk):
    r = get_object_or_404(Reservation, pk=pk)
    if request.method == "POST":
        form = CancellationForm(request.POST)
        if form.is_valid():
            cancellation.request_cancellation(r, request.user, form.cleaned_data["reason"])
            messages.success(request, "تم التعامل مع طلب الإلغاء.")
    return redirect("reservations:detail", pk)


@login_required
def delay_request_create(request, pk):
    r = get_object_or_404(Reservation, pk=pk)
    if request.method == "POST":
        form = DelayRequestForm(request.POST)
        if form.is_valid():
            delay.create_delay_request(r, request.user, form.cleaned_data["minutes"])
            messages.success(request, "تم إرسال طلب التأخير.")
    return redirect("reservations:detail", pk)


@login_required
def delay_request_respond(request, pk, accept):
    d = get_object_or_404(DelayRequest, pk=pk)
    delay.respond_to_delay(d, request.user, bool(int(accept)))
    return redirect("reservations:detail", d.reservation_id)


@login_required
def mark_passenger_no_show(request, pk):
    no_show.mark_passenger_no_show(get_object_or_404(Reservation, pk=pk), request.user)
    return redirect("reservations:detail", pk)


@login_required
def mark_driver_no_show(request, pk):
    no_show.mark_driver_no_show(get_object_or_404(Reservation, pk=pk), request.user)
    return redirect("reservations:detail", pk)


@login_required
def dispute_create(request, pk):
    from apps.disputes.services import open_dispute
    r = get_object_or_404(Reservation, pk=pk)
    form = DisputeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        open_dispute(r, request.user, form.cleaned_data["category"], form.cleaned_data["description"])
    return redirect("reservations:detail", pk)
