from .models import Notification
MESSAGES={"reservation_created":"تم إنشاء الحجز بنجاح.","reservation_confirmed":"تم تأكيد الحجز من قبل السائق.","driver_on_the_way":"السائق في الطريق إليك.","driver_arrived":"وصل السائق إلى نقطة الانطلاق.","waiting_started":"بدأت فترة الانتظار.","reservation_in_progress":"بدأت الرحلة.","reservation_completed":"اكتملت الرحلة.","reservation_cancelled":"تم إلغاء الحجز.","passenger_no_show":"تم تسجيل عدم حضور الراكب.","driver_no_show":"تم تسجيل عدم حضور السائق.","reservation_disputed":"تم فتح نزاع على هذا الحجز.","delay_requested":"تم استلام طلب تأخير جديد.","delay_accepted":"تمت الموافقة على طلب التأخير.","delay_rejected":"تم رفض طلب التأخير."}
def notify(recipient,verb,*,reservation=None,message=None): return Notification.objects.create(recipient=recipient,verb=verb,message=message or MESSAGES.get(verb,verb),reservation=reservation)
def notify_reservation_status_change(reservation,from_status,to_status):
    verb={"confirmed":"reservation_confirmed","driver_on_the_way":"driver_on_the_way","driver_arrived":"driver_arrived","waiting":"waiting_started","in_progress":"reservation_in_progress","completed":"reservation_completed","cancelled":"reservation_cancelled","passenger_no_show":"passenger_no_show","driver_no_show":"driver_no_show","disputed":"reservation_disputed"}.get(to_status)
    if not verb:return
    for user in (reservation.passenger,reservation.driver):
        if user: notify(user,verb,reservation=reservation)
