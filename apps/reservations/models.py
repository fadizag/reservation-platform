from django.conf import settings
from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel

class Reservation(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING="pending","بانتظار سائق"; CONFIRMED="confirmed","مؤكدة"; DRIVER_ON_THE_WAY="driver_on_the_way","السائق في الطريق"; DRIVER_ARRIVED="driver_arrived","السائق وصل"; WAITING="waiting","بانتظار الراكب"; IN_PROGRESS="in_progress","الرحلة جارية"; COMPLETED="completed","مكتملة"; CANCELLED="cancelled","ملغاة"; PASSENGER_NO_SHOW="passenger_no_show","الراكب لم يحضر"; DRIVER_NO_SHOW="driver_no_show","السائق لم يحضر"; DISPUTED="disputed","قيد النزاع"
    passenger=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="reservations_as_passenger",limit_choices_to={"role":"passenger"})
    driver=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="reservations_as_driver",null=True,blank=True,limit_choices_to={"role":"driver"})
    pickup=models.ForeignKey("locations.Location",on_delete=models.PROTECT,related_name="+")
    destination=models.ForeignKey("locations.Location",on_delete=models.PROTECT,related_name="+")
    scheduled_time=models.DateTimeField(); seats_requested=models.PositiveSmallIntegerField(default=1); additional_info=models.TextField(blank=True)
    status=models.CharField(max_length=32,choices=Status.choices,default=Status.PENDING)
    driver_departed_at=models.DateTimeField(null=True,blank=True); driver_arrived_at=models.DateTimeField(null=True,blank=True); waiting_started_at=models.DateTimeField(null=True,blank=True); waiting_deadline=models.DateTimeField(null=True,blank=True); passenger_checked_in_at=models.DateTimeField(null=True,blank=True); started_at=models.DateTimeField(null=True,blank=True); completed_at=models.DateTimeField(null=True,blank=True); cancelled_at=models.DateTimeField(null=True,blank=True)
    class Meta: ordering=["-scheduled_time"]
    def __str__(self): return f"Reservation #{self.pk} ({self.get_status_display()})"
    @property
    def is_locked_for_normal_changes(self):
        from apps.core.models import PlatformSettings
        return timezone.now() >= self.scheduled_time-timezone.timedelta(minutes=PlatformSettings.get_solo().lock_period_minutes)
    @property
    def active_delay_request(self): return self.delay_requests.filter(status=DelayRequest.Status.PENDING).first()
    @property
    def has_accepted_delay(self): return self.delay_requests.filter(status=DelayRequest.Status.ACCEPTED).exists()
    @property
    def has_active_dispute(self): return self.disputes.filter(status__in=["open","under_review"]).exists() if hasattr(self,"disputes") else False

class ReservationEvent(TimeStampedModel):
    reservation=models.ForeignKey(Reservation,on_delete=models.CASCADE,related_name="events"); actor=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name="reservation_events"); previous_status=models.CharField(max_length=32,blank=True); new_status=models.CharField(max_length=32,blank=True); event_type=models.CharField(max_length=64); reason=models.CharField(max_length=255,blank=True); metadata=models.JSONField(default=dict,blank=True); occurred_at=models.DateTimeField(default=timezone.now)
    class Meta: ordering=["occurred_at"]

class DelayRequest(TimeStampedModel):
    class RequestedBy(models.TextChoices): PASSENGER="passenger","Passenger"; DRIVER="driver","Driver"
    class Status(models.TextChoices): PENDING="pending","بانتظار الرد"; ACCEPTED="accepted","مقبول"; REJECTED="rejected","مرفوض"; EXPIRED="expired","منتهي الصلاحية"
    reservation=models.ForeignKey(Reservation,on_delete=models.CASCADE,related_name="delay_requests"); requested_by=models.CharField(max_length=16,choices=RequestedBy.choices); requested_by_user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="+"); minutes_requested=models.PositiveSmallIntegerField(); status=models.CharField(max_length=16,choices=Status.choices,default=Status.PENDING); responded_at=models.DateTimeField(null=True,blank=True); expires_at=models.DateTimeField()

class CancellationExceptionRequest(TimeStampedModel):
    class Status(models.TextChoices): PENDING="pending","بانتظار المراجعة"; APPROVED="approved","موافق عليه"; DENIED="denied","مرفوض"
    reservation=models.ForeignKey(Reservation,on_delete=models.CASCADE,related_name="exception_requests"); requested_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="+"); reason=models.TextField(); status=models.CharField(max_length=16,choices=Status.choices,default=Status.PENDING); resolved_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="+"); resolved_at=models.DateTimeField(null=True,blank=True); resolution_note=models.TextField(blank=True)
