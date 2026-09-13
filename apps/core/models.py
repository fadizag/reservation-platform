from django.core.exceptions import ValidationError
from django.db import models


class TimeStampedModel(models.Model):
    """Abstract base: every domain row records when it was created/touched."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PlatformSettings(models.Model):
    """Singleton row holding admin-configurable business rules."""

    lock_period_minutes = models.PositiveIntegerField(default=30)
    max_waiting_minutes = models.PositiveIntegerField(default=10)
    delay_request_max_minutes = models.PositiveIntegerField(default=20)
    no_show_requires_admin_review = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Platform settings"
        verbose_name_plural = "Platform settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    def clean(self):
        if PlatformSettings.objects.exclude(pk=self.pk).exists():
            raise ValidationError("Only one PlatformSettings row may exist.")

    @classmethod
    def get_solo(cls) -> "PlatformSettings":
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Platform settings"
