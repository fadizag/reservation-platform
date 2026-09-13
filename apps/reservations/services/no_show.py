from django.core.exceptions import PermissionDenied
from django.utils import timezone
from apps.reservations.models import Reservation
from . import state_machine

def check_passenger_no_show_eligible(r):
    failures=[]; now=timezone.now()
    if r.status!=Reservation.Status.WAITING: failures.append("الحجز ليس في حالة انتظار.")
    if not r.waiting_started_at: failures.append("لم تبدأ فترة الانتظار.")
    if r.waiting_deadline and now<r.waiting_deadline: failures.append("فترة الانتظار لم تنتهِ.")
    if r.has_accepted_delay: failures.append("يوجد تأخير مقبول لم ينتهِ بعد.")
    return failures

def check_driver_no_show_eligible(r):
    failures=[]
    if r.status not in {Reservation.Status.CONFIRMED,Reservation.Status.DRIVER_ON_THE_WAY}: failures.append("الحجز غير مؤهل لتسجيل عدم حضور السائق.")
    if r.driver_arrived_at: failures.append("السائق مسجل كواصل بالفعل.")
    return failures

def mark_passenger_no_show(r,user):
    if user!=r.driver: raise PermissionDenied("Only the assigned driver can report passenger no-show.")
    failures=check_passenger_no_show_eligible(r)
    if failures: raise PermissionDenied(" ".join(failures))
    return state_machine.transition(r,Reservation.Status.PASSENGER_NO_SHOW,actor=user,reason="Passenger no-show")

def mark_driver_no_show(r,user):
    if user!=r.passenger: raise PermissionDenied("Only the passenger can report driver no-show.")
    failures=check_driver_no_show_eligible(r)
    if failures: raise PermissionDenied(" ".join(failures))
    return state_machine.transition(r,Reservation.Status.DRIVER_NO_SHOW,actor=user,reason="Driver no-show")
