from django.conf import settings
from django.db import models
from apps.core.models import TimeStampedModel
class Notification(TimeStampedModel):
    recipient=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="notifications"); reservation=models.ForeignKey("reservations.Reservation",on_delete=models.CASCADE,null=True,blank=True,related_name="notifications"); verb=models.CharField(max_length=64); message=models.TextField(); is_read=models.BooleanField(default=False)
    class Meta: ordering=["-created_at"]
class WebPushSubscription(TimeStampedModel):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="push_subscriptions"); endpoint=models.URLField(max_length=500); p256dh_key=models.CharField(max_length=255); auth_key=models.CharField(max_length=255)
    class Meta: unique_together=("user","endpoint")
