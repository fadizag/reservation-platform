from django.conf import settings
from django.db import models
from apps.core.models import TimeStampedModel
class Transaction(TimeStampedModel):
    class Type(models.TextChoices): DEPOSIT_CAPTURE="deposit_capture","Deposit"; DRIVER_EARNING="driver_earning","Driver earning"; REFUND="refund","Refund"; PENALTY="penalty","Penalty"
    class Status(models.TextChoices): PENDING="pending","Pending"; SUCCEEDED="succeeded","Succeeded"; FAILED="failed","Failed"
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="transactions"); reservation=models.ForeignKey("reservations.Reservation",on_delete=models.PROTECT,related_name="transactions",null=True,blank=True); type=models.CharField(max_length=32,choices=Type.choices); amount=models.DecimalField(max_digits=12,decimal_places=2); status=models.CharField(max_length=16,choices=Status.choices,default=Status.SUCCEEDED); description=models.CharField(max_length=255,blank=True)
    class Meta: ordering=["-created_at"]
