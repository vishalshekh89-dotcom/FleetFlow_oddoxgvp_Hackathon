from django.db import models

class Vehicle(models.Model):
    VEHICLE_TYPE = [
        ('truck', 'Truck'),
        ('van', 'Van'),
        ('bike', 'Bike'),
    ]
    STATUS = [
        ('available', 'Available'),
        ('on_trip', 'On Trip'),
        ('in_shop', 'In Shop'),
        ('retired', 'Retired'),
    ]

    name = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE)
    max_capacity_kg = models.FloatField()
    odometer = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=STATUS, default='available')
    region = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.license_plate})"

    def status_badge(self):
        badges = {
            'available': 'success',
            'on_trip': 'primary',
            'in_shop': 'warning',
            'retired': 'secondary',
        }
        return badges.get(self.status, 'secondary')