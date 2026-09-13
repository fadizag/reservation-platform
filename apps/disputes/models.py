from django.conf import settings
from django.db import models
from apps.core.models import TimeStampedModel
class Dispute(TimeStampedModel):
    class Category(models.TextChoices): NO_SHOW="no_show","عدم حضور"; DELAY="delay","تأخير"; BEHAVIOR="behavior","سلوك"; PAYMENT="payment","مالي"; OTHER="other","أخرى"
    class Status(models.TextChoices): OPEN="open","مفتوح"; UNDER_REVIEW="under_review","قيد المراجعة"; RESOLVED="resolved","تم الحل"; REJECTED="rejected","مرفوض"
    reservation=models.ForeignKey("reservations.Reservation",on_delete=models.CASCADE,related_name="disputes"); raised_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="disputes_raised"); category=models.CharField(max_length=32,choices=Category.choices); description=models.TextField(); status=models.CharField(max_length=16,choices=Status.choices,default=Status.OPEN); resolution_note=models.TextField(blank=True); resolved_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="+"); resolved_at=models.DateTimeField(null=True,blank=True)
class DisputeAttachment(TimeStampedModel):
    dispute=models.ForeignKey(Dispute,on_delete=models.CASCADE,related_name="attachments"); file=models.FileField(upload_to="dispute_evidence/%Y/%m/"); uploaded_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="+")
