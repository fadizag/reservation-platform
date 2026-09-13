from django.utils import timezone
from apps.notifications.services import notify_reservation_status_change
from apps.reservations.models import Reservation,ReservationEvent
Status=Reservation.Status
class InvalidTransition(Exception): pass
ALLOWED_TRANSITIONS={Status.PENDING:{Status.CONFIRMED,Status.CANCELLED},Status.CONFIRMED:{Status.DRIVER_ON_THE_WAY,Status.CANCELLED,Status.DRIVER_NO_SHOW,Status.DISPUTED},Status.DRIVER_ON_THE_WAY:{Status.DRIVER_ARRIVED,Status.CANCELLED,Status.DRIVER_NO_SHOW,Status.DISPUTED},Status.DRIVER_ARRIVED:{Status.WAITING,Status.DISPUTED},Status.WAITING:{Status.IN_PROGRESS,Status.PASSENGER_NO_SHOW,Status.CANCELLED,Status.DISPUTED},Status.IN_PROGRESS:{Status.COMPLETED,Status.DISPUTED},Status.DISPUTED:{Status.CANCELLED,Status.COMPLETED,Status.PASSENGER_NO_SHOW,Status.DRIVER_NO_SHOW},Status.COMPLETED:set(),Status.CANCELLED:set(),Status.PASSENGER_NO_SHOW:set(),Status.DRIVER_NO_SHOW:set()}
def transition(reservation,to_status,*,actor=None,reason="",event_type="status_change",metadata=None):
    from_status=reservation.status
    if to_status==from_status or to_status not in ALLOWED_TRANSITIONS.get(from_status,set()): raise InvalidTransition(f"Cannot move reservation #{reservation.pk} from '{from_status}' to '{to_status}'.")
    now=timezone.now(); reservation.status=to_status
    if to_status==Status.CANCELLED: reservation.cancelled_at=now
    elif to_status==Status.DRIVER_ON_THE_WAY: reservation.driver_departed_at=now
    elif to_status==Status.DRIVER_ARRIVED: reservation.driver_arrived_at=now
    elif to_status==Status.WAITING: reservation.waiting_started_at=now
    elif to_status==Status.IN_PROGRESS: reservation.passenger_checked_in_at=reservation.passenger_checked_in_at or now; reservation.started_at=now
    elif to_status==Status.COMPLETED: reservation.completed_at=now
    reservation.save()
    ReservationEvent.objects.create(reservation=reservation,actor=actor,previous_status=from_status,new_status=to_status,event_type=event_type,reason=reason,metadata=metadata or {},occurred_at=now)
    notify_reservation_status_change(reservation,from_status,to_status)
    return reservation
