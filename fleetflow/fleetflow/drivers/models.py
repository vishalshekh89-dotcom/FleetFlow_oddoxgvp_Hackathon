from django.db import models
from datetime import date

class Driver(models.Model):
    STATUS = [
        ('on_duty', 'On Duty'),
        ('off_duty', 'Off Duty'),
        ('suspended', 'Suspended'),
    ]
    LICENSE_CAT = [
        ('truck', 'Truck'),
        ('van', 'Van'),
        ('bike', 'Bike'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry = models.DateField()
    license_category = models.CharField(max_length=10, choices=LICENSE_CAT)
    safety_score = models.FloatField(default=100.0)
    status = models.CharField(max_length=20, choices=STATUS, default='off_duty')
    created_at = models.DateTimeField(auto_now_add=True)

    def is_license_valid(self):
        return self.license_expiry >= date.today()

    def status_badge(self):
        badges = {
            'on_duty': 'success',
            'off_duty': 'secondary',
            'suspended': 'danger',
        }
        return badges.get(self.status, 'secondary')

    def __str__(self):
        return self.name