# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from trips.models import Trip
# from expenses.models import FuelLog
# from maintenance.models import MaintenanceLog
# from vehicles.models import Vehicle
# from django.db.models import Sum
# import csv
# from django.http import HttpResponse


# @login_required
# def analytics(request):
#     total_trips = Trip.objects.filter(status='completed').count()
#     total_fuel = FuelLog.objects.aggregate(t=Sum('cost'))['t'] or 0
#     total_maintenance = MaintenanceLog.objects.aggregate(t=Sum('cost'))['t'] or 0

#     completed_trips = Trip.objects.filter(status='completed', end_odometer__isnull=False)
#     total_km = sum([t.distance_km() for t in completed_trips]) or 1
#     total_liters = FuelLog.objects.aggregate(t=Sum('liters'))['t'] or 1

#     avg_fuel_efficiency = round(total_km / float(total_liters), 1)
#     avg_cost_per_km = round((float(total_fuel) + float(total_maintenance)) / total_km, 1)

#     # Per vehicle summary
#     vehicle_summary = []
#     for v in Vehicle.objects.all():
#         fuel = FuelLog.objects.filter(vehicle=v).aggregate(t=Sum('cost'))['t'] or 0
#         maint = MaintenanceLog.objects.filter(vehicle=v).aggregate(t=Sum('cost'))['t'] or 0
#         trips = Trip.objects.filter(vehicle=v, status='completed').count()
#         vehicle_summary.append({
#             'name': v.name,
#             'fuel_total': fuel,
#             'maint_total': maint,
#             'total': float(fuel) + float(maint),
#             'trip_count': trips,
#         })

#     context = {
#         'total_trips': total_trips,
#         'avg_fuel_efficiency': avg_fuel_efficiency,
#         'avg_cost_per_km': avg_cost_per_km,
#         'vehicle_summary': vehicle_summary,
#     }
#     return render(request, 'analytics/analytics.html', context)



# @login_required
# def export_csv(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="fleetflow_report.csv"'
#     writer = csv.writer(response)
#     writer.writerow(['Vehicle', 'Fuel Cost', 'Maintenance Cost', 'Total Cost', 'Trips Completed'])
#     for v in Vehicle.objects.all():
#         fuel = FuelLog.objects.filter(vehicle=v).aggregate(t=Sum('cost'))['t'] or 0
#         maint = MaintenanceLog.objects.filter(vehicle=v).aggregate(t=Sum('cost'))['t'] or 0
#         trips = Trip.objects.filter(vehicle=v, status='completed').count()
#         writer.writerow([v.name, fuel, maint, float(fuel)+float(maint), trips])
#     return response



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from trips.models import Trip
from expenses.models import FuelLog
from maintenance.models import MaintenanceLog
from vehicles.models import Vehicle
from django.db.models import Sum
import csv
from django.http import HttpResponse

def get_group(user):
    if user.is_superuser:
        return 'Manager'
    group = user.groups.first()
    return group.name if group else ''

def redirect_user(group):
    if group == 'Dispatcher':
        return redirect('trip_list')
    elif group == 'Safety Officer':
        return redirect('driver_list')
    return redirect('dashboard')

@login_required
def analytics(request):
    group = get_group(request.user)
    if group not in ['Manager', 'Analyst']:
        messages.error(request, 'Access Denied!')
        return redirect_user(group)

    total_trips = Trip.objects.filter(status='completed').count()
    total_fuel = FuelLog.objects.aggregate(t=Sum('cost'))['t'] or 0
    total_maintenance = MaintenanceLog.objects.aggregate(t=Sum('cost'))['t'] or 0

    completed_trips = Trip.objects.filter(
        status='completed', end_odometer__isnull=False
    )
    total_km = sum([t.distance_km() for t in completed_trips]) or 1
    total_liters = float(FuelLog.objects.aggregate(t=Sum('liters'))['t'] or 1)

    avg_fuel_efficiency = round(total_km / total_liters, 1)
    avg_cost_per_km = round(
        (float(total_fuel) + float(total_maintenance)) / total_km, 1
    )

    vehicle_summary = []
    for v in Vehicle.objects.all():
        fuel = FuelLog.objects.filter(vehicle=v).aggregate(t=Sum('cost'))['t'] or 0
        maint = MaintenanceLog.objects.filter(vehicle=v).aggregate(t=Sum('cost'))['t'] or 0
        trips = Trip.objects.filter(vehicle=v, status='completed').count()
        vehicle_summary.append({
            'name': v.name,
            'fuel_total': fuel,
            'maint_total': maint,
            'total': float(fuel) + float(maint),
            'trip_count': trips,
        })

    context = {
        'total_trips': total_trips,
        'avg_fuel_efficiency': avg_fuel_efficiency,
        'avg_cost_per_km': avg_cost_per_km,
        'vehicle_summary': vehicle_summary,
    }
    return render(request, 'analytics/analytics.html', context)

@login_required
def export_csv(request):
    group = get_group(request.user)
    if group not in ['Manager', 'Analyst']:
        return redirect_user(group)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fleetflow_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Vehicle', 'Fuel Cost', 'Maintenance Cost', 'Total Cost', 'Trips'])
    for v in Vehicle.objects.all():
        fuel = FuelLog.objects.filter(vehicle=v).aggregate(t=Sum('cost'))['t'] or 0
        maint = MaintenanceLog.objects.filter(vehicle=v).aggregate(t=Sum('cost'))['t'] or 0
        trips = Trip.objects.filter(vehicle=v, status='completed').count()
        writer.writerow([v.name, fuel, maint, float(fuel) + float(maint), trips])
    return response