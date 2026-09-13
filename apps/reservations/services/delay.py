from django.core.exceptions import PermissionDenied,ValidationError
from django.utils import timezone
from apps.core.models import PlatformSettings
from apps.reservations.models import DelayRequest,Reservation
from apps.notifications.services import notify

def create_delay_request(reservation,user,minutes):
    if user not in (reservation.passenger,reservation.driver): raise PermissionDenied("Not a party to this reservation.")
    if minutes<1 or minutes>PlatformSettings.get_solo().delay_request_max_minutes: raise ValidationError("Invalid delay duration.")
    if reservation.active_delay_request: raise ValidationError("There is already a pending delay request.")
    requested_by="passenger" if user==reservation.passenger else "driver"
    obj=DelayRequest.objects.create(reservation=reservation,requested_by=requested_by,requested_by_user=user,minutes_requested=minutes,expires_at=timezone.now()+timezone.timedelta(minutes=5))
    other=reservation.driver if requested_by=="passenger" else reservation.passenger
    if other: notify(other,"delay_requested",reservation=reservation)
    return obj

def respond_to_delay(delay_request,user,accept):
    r=delay_request.reservation
    if user not in (r.passenger,r.driver): raise PermissionDenied("Not a party to this reservation.")
    if delay_request.status!=DelayRequest.Status.PENDING: raise ValidationError("Delay request is no longer pending.")
    if user==delay_request.requested_by_user: raise PermissionDenied("The requester cannot respond to their own request.")
    delay_request.status=DelayRequest.Status.ACCEPTED if accept else DelayRequest.Status.REJECTED; delay_request.responded_at=timezone.now(); delay_request.save()
    if accept and r.waiting_deadline: r.waiting_deadline+=timezone.timedelta(minutes=delay_request.minutes_requested); r.save(update_fields=["waiting_deadline"])
    notify(delay_request.requested_by_user,"delay_accepted" if accept else "delay_rejected",reservation=r)
    return delay_request

def expire_stale_delay_requests():
    qs=DelayRequest.objects.filter(status=DelayRequest.Status.PENDING,expires_at__lte=timezone.now()); count=qs.update(status=DelayRequest.Status.EXPIRED,responded_at=timezone.now()); return count
