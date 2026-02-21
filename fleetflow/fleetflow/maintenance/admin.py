from django.contrib import admin
from .models import MaintenanceLog

@admin.register(MaintenanceLog)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'description', 'cost', 'date']
    list_filter = ['date', 'vehicle']
    search_fields = ['vehicle__name', 'description']