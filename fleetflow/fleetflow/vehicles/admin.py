from django.contrib import admin
from .models import Vehicle

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['name', 'license_plate', 'vehicle_type', 'max_capacity_kg', 'status', 'region']
    list_filter = ['status', 'vehicle_type']
    search_fields = ['name', 'license_plate']
    list_editable = ['status']