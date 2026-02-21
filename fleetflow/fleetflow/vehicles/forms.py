from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['name', 'license_plate', 'vehicle_type', 'max_capacity_kg', 'odometer', 'region', 'status']