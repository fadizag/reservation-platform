from django import forms
from apps.disputes.models import Dispute
from apps.locations.models import Location
from apps.reservations.models import Reservation


class ReservationCreateForm(forms.Form):
    pickup_label = forms.CharField(label="عنوان الانطلاق", max_length=255)
    pickup_lat = forms.DecimalField(max_digits=9, decimal_places=6, widget=forms.HiddenInput(attrs={"data-location-field": "pickup"}))
    pickup_lng = forms.DecimalField(max_digits=9, decimal_places=6, widget=forms.HiddenInput(attrs={"data-location-field": "pickup"}))
    destination_label = forms.CharField(label="عنوان الوجهة", max_length=255)
    destination_lat = forms.DecimalField(max_digits=9, decimal_places=6, widget=forms.HiddenInput(attrs={"data-location-field": "destination"}))
    destination_lng = forms.DecimalField(max_digits=9, decimal_places=6, widget=forms.HiddenInput(attrs={"data-location-field": "destination"}))
    scheduled_time = forms.DateTimeField(label="موعد الرحلة", widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))
    seats_requested = forms.IntegerField(label="عدد المقاعد", min_value=1, max_value=8, initial=1)
    additional_info = forms.CharField(label="معلومات إضافية", required=False, widget=forms.Textarea(attrs={"rows": 3}))

    def clean(self):
        cleaned = super().clean()
        for prefix, label in (("pickup", "الانطلاق"), ("destination", "الوجهة")):
            if cleaned.get(f"{prefix}_lat") is None or cleaned.get(f"{prefix}_lng") is None:
                raise forms.ValidationError(f"حدد موقع {label} على الخريطة قبل المتابعة.")
        return cleaned

    def save(self, passenger):
        d = self.cleaned_data
        pickup = Location.objects.create(label=d["pickup_label"], latitude=d["pickup_lat"], longitude=d["pickup_lng"])
        destination = Location.objects.create(label=d["destination_label"], latitude=d["destination_lat"], longitude=d["destination_lng"])
        return Reservation.objects.create(passenger=passenger, pickup=pickup, destination=destination, scheduled_time=d["scheduled_time"], seats_requested=d["seats_requested"], additional_info=d["additional_info"])


class DelayRequestForm(forms.Form):
    minutes = forms.IntegerField(label="عدد الدقائق الإضافية", min_value=1, max_value=60)


class CancellationForm(forms.Form):
    reason = forms.CharField(label="سبب الإلغاء", required=False, widget=forms.Textarea(attrs={"rows": 2}))


class DisputeForm(forms.ModelForm):
    class Meta:
        model = Dispute
        fields = ["category", "description"]
