from django.core.exceptions import PermissionDenied
from django.utils import timezone
from apps.core.models import PlatformSettings
from apps.reservations.models import CancellationExceptionRequest,Reservation
from . import state_machine

def request_cancellation(reservation,user,reason=""):
    if user not in (reservation.passenger,reservation.driver) and not user.is_admin_role: raise PermissionDenied("You cannot cancel this reservation.")
    if reservation.is_locked_for_normal_changes and not user.is_admin_role:
        return CancellationExceptionRequest.objects.create(reservation=reservation,requested_by=user,reason=reason)
    state_machine.transition(reservation,Reservation.Status.CANCELLED,actor=user,reason=reason or "Cancelled")
    return reservation

def resolve_exception_request(exception_request,admin_user,approve,note=""):
    if not admin_user.is_admin_role: raise PermissionDenied("Admin access required.")
    exception_request.status=CancellationExceptionRequest.Status.APPROVED if approve else CancellationExceptionRequest.Status.DENIED; exception_request.resolved_by=admin_user; exception_request.resolved_at=timezone.now(); exception_request.resolution_note=note; exception_request.save()
    if approve and exception_request.reservation.status not in {Reservation.Status.CANCELLED,Reservation.Status.COMPLETED}: state_machine.transition(exception_request.reservation,Reservation.Status.CANCELLED,actor=admin_user,reason=note or "Exception approved")
    return exception_request
