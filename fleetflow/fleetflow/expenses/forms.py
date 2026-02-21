from django import forms
from .models import FuelLog

class FuelLogForm(forms.ModelForm):
    class Meta:
        model = FuelLog
        fields = ['vehicle', 'trip', 'liters', 'cost', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }