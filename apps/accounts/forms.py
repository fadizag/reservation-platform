from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
class SignUpForm(UserCreationForm):
    role=forms.ChoiceField(choices=[(User.Role.PASSENGER,"راكب"),(User.Role.DRIVER,"سائق")],label="نوع الحساب")
    phone_number=forms.CharField(label="رقم الهاتف")
    class Meta:
        model=User
        fields=("username","phone_number","role","password1","password2")
    def save(self,commit=True):
        user=super().save(commit=False); user.phone_number=self.cleaned_data["phone_number"]; user.role=self.cleaned_data["role"]
        if commit: user.save()
        return user
