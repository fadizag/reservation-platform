from django.core.exceptions import PermissionDenied
from django.utils import timezone
from apps.disputes.models import Dispute
from apps.reservations.models import Reservation
from apps.reservations.services import state_machine

def open_dispute(reservation,raised_by,category,description):
    if raised_by not in (reservation.passenger,reservation.driver): raise PermissionDenied("Only the passenger or driver may open a dispute.")
    dispute=Dispute.objects.create(reservation=reservation,raised_by=raised_by,category=category,description=description)
    if reservation.status not in {Reservation.Status.COMPLETED,Reservation.Status.CANCELLED}:
        try: state_machine.transition(reservation,Reservation.Status.DISPUTED,actor=raised_by,reason=f"Dispute opened: {category}",event_type="dispute_opened",metadata={"dispute_id":dispute.pk})
        except state_machine.InvalidTransition: pass
    return dispute

def resolve_dispute(dispute,admin_user,status,note=""):
    dispute.status=status; dispute.resolution_note=note; dispute.resolved_by=admin_user; dispute.resolved_at=timezone.now(); dispute.save(); return dispute
