from django import forms
from .models import Trip

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['vehicle', 'driver', 'cargo_weight_kg', 'origin', 'destination', 'start_odometer', 'notes']