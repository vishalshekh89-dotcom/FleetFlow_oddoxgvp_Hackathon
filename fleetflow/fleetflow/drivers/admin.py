from django.contrib import admin
from .models import Driver

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'license_number', 'license_expiry', 'license_category', 'status', 'safety_score']
    list_filter = ['status', 'license_category']
    search_fields = ['name', 'license_number']
    list_editable = ['status']