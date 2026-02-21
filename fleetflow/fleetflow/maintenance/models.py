from django.db import models
from vehicles.models import Vehicle

class MaintenanceLog(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto Logic: Vehicle → In Shop
        self.vehicle.status = 'in_shop'
        self.vehicle.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Maintenance - {self.vehicle.name} on {self.date}"