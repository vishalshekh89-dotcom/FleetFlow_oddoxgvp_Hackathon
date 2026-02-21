from django.db import models
from vehicles.models import Vehicle
from drivers.models import Driver

class Trip(models.Model):
    STATUS = [
        ('draft', 'Draft'),
        ('dispatched', 'Dispatched'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT)
    cargo_weight_kg = models.FloatField()
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    start_odometer = models.FloatField()
    end_odometer = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def distance_km(self):
        if self.end_odometer:
            return self.end_odometer - self.start_odometer
        return 0

    def status_badge(self):
        badges = {
            'draft': 'secondary',
            'dispatched': 'primary',
            'completed': 'success',
            'cancelled': 'danger',
        }
        return badges.get(self.status, 'secondary')

    def __str__(self):
        return f"Trip #{self.id} — {self.origin} → {self.destination}"