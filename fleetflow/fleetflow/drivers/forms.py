from django import forms
from .models import Driver

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'phone', 'license_number', 'license_expiry', 'license_category', 'safety_score', 'status']
        widgets = {
            'license_expiry': forms.DateInput(attrs={'type': 'date'}),
        }