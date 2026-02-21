
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from trips.models import Trip
# from expenses.models import FuelLog
# from maintenance.models import MaintenanceLog
# from vehicles.models import Vehicle
# from django.db.models import Sum
# import csv
# from django.http import HttpResponse

# def get_group(user):
#     if user.is_superuser:
#         return 'Manager'
#     group = user.groups.first()
#     return group.name if group else ''

# def redirect_user(group):
#     if group == 'Dispatcher':
#         return redirect('trip_list')
#     elif group == 'Safety Officer':
#         return redirect('driver_list')
#     return redirect('dashboard')

# @login_required
# def analytics(request):
#     group = get_group(request.user)
#     if group not in ['Manager', 'Analyst']:
#         messages.error(request, 'Access Denied!')
#         return redirect_user(group)

#     total_trips = Trip.objects.filter(status='completed').count()
#     total_fuel = FuelLog.objects.aggregate(t=Sum('cost'))['t'] or 0
#     total_maintenance = MaintenanceLog.objects.aggregate(t=Sum('cost'))['t'] or 0

#     completed_trips = Trip.objects.filter(
#         status='completed', end_odometer__isnull=False
#     )
#     total_km = sum([t.distance_km() for t in completed_trips]) or 1
#     total_liters = float(FuelLog.objects.aggregate(t=Sum('liters'))['t'] or 1)

#     avg_fuel_efficiency = round(total_km / total_liters, 1)
#     avg_cost_per_km = round(
#         (float(total_fuel) + float(total_maintenance)) / total_km, 1
#     )

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
#     group = get_group(request.user)
#     if group not in ['Manager', 'Analyst']:
#         return redirect_user(group)

#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="fleetflow_report.csv"'
#     writer = csv.writer(response)
#     writer.writerow(['Vehicle', 'Fuel Cost', 'Maintenance Cost', 'Total Cost', 'Trips'])
#     for v in Vehicle.objects.all():
#         fuel = FuelLog.objects.filter(vehicle=v).aggregate(t=Sum('cost'))['t'] or 0
#         maint = MaintenanceLog.objects.filter(vehicle=v).aggregate(t=Sum('cost'))['t'] or 0
#         trips = Trip.objects.filter(vehicle=v, status='completed').count()
#         writer.writerow([v.name, fuel, maint, float(fuel) + float(maint), trips])
#     return response

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from trips.models import Trip
from expenses.models import FuelLog
from maintenance.models import MaintenanceLog
from vehicles.models import Vehicle
from django.db.models import Sum
from django.utils import timezone
import csv
from django.http import HttpResponse
from collections import defaultdict

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

    # ── KPI ──
    total_fuel = float(FuelLog.objects.aggregate(t=Sum('cost'))['t'] or 0)
    total_maint = float(MaintenanceLog.objects.aggregate(t=Sum('cost'))['t'] or 0)
    total_cost = total_fuel + total_maint

    total_vehicles = Vehicle.objects.count() or 1
    on_trip_count = Vehicle.objects.filter(status='on_trip').count()
    utilization_rate = round((on_trip_count / total_vehicles) * 100)

    completed_trips = Trip.objects.filter(status='completed', end_odometer__isnull=False)
    total_km = sum([t.distance_km() for t in completed_trips]) or 1
    total_liters = float(FuelLog.objects.aggregate(t=Sum('liters'))['t'] or 1)
    avg_fuel_efficiency = round(total_km / total_liters, 1)
    avg_cost_per_km = round(total_cost / total_km, 1)
    total_trips = Trip.objects.filter(status='completed').count()

    # Fleet ROI (dummy: revenue estimate = trips * avg 500km * Rs8/km)
    estimated_revenue = total_trips * 500 * 8
    roi = round(((estimated_revenue - total_cost) / total_cost * 100), 1) if total_cost else 0

    # ── TOP 5 COSTLIEST VEHICLES ──
    vehicle_summary = []
    for v in Vehicle.objects.all():
        fuel = float(FuelLog.objects.filter(vehicle=v).aggregate(t=Sum('cost'))['t'] or 0)
        maint = float(MaintenanceLog.objects.filter(vehicle=v).aggregate(t=Sum('cost'))['t'] or 0)
        trips = Trip.objects.filter(vehicle=v, status='completed').count()
        vehicle_summary.append({
            'name': v.name,
            'fuel_total': fuel,
            'maint_total': maint,
            'total': fuel + maint,
            'trip_count': trips,
        })

    top5 = sorted(vehicle_summary, key=lambda x: x['total'], reverse=True)[:5]

    # ── FUEL EFFICIENCY TREND (last 6 months) ──
    months = []
    efficiency_data = []
    today = timezone.now()
    for i in range(5, -1, -1):
        m = (today.month - i - 1) % 12 + 1
        y = today.year - ((today.month - i - 1) // 12)
        label = f"{['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][m-1]}"
        months.append(label)
        fuel_l = float(FuelLog.objects.filter(date__month=m, date__year=y).aggregate(t=Sum('liters'))['t'] or 0)
        trips_m = Trip.objects.filter(status='completed', end_odometer__isnull=False, created_at__month=m, created_at__year=y)
        km_m = sum([t.distance_km() for t in trips_m]) or 0
        eff = round(km_m / fuel_l, 1) if fuel_l > 0 else 0
        efficiency_data.append(eff)

    # ── MONTHLY FINANCIAL SUMMARY ──
    monthly_summary = []
    for i in range(5, -1, -1):
        m = (today.month - i - 1) % 12 + 1
        y = today.year - ((today.month - i - 1) // 12)
        label = f"{['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][m-1]} {y}"
        fuel_cost = float(FuelLog.objects.filter(date__month=m, date__year=y).aggregate(t=Sum('cost'))['t'] or 0)
        maint_cost = float(MaintenanceLog.objects.filter(date__month=m, date__year=y).aggregate(t=Sum('cost'))['t'] or 0)
        trips_m = Trip.objects.filter(status='completed', created_at__month=m, created_at__year=y).count()
        revenue = trips_m * 500 * 8
        net = revenue - fuel_cost - maint_cost
        if fuel_cost > 0 or maint_cost > 0 or trips_m > 0:
            monthly_summary.append({
                'month': label,
                'revenue': revenue,
                'fuel': fuel_cost,
                'maint': maint_cost,
                'net': net,
            })

    context = {
        # KPI
        'total_fuel': total_fuel,
        'total_maint': total_maint,
        'total_cost': total_cost,
        'utilization_rate': utilization_rate,
        'roi': roi,
        'avg_fuel_efficiency': avg_fuel_efficiency,
        'avg_cost_per_km': avg_cost_per_km,
        'total_trips': total_trips,
        # Charts
        'top5': top5,
        'months': months,
        'efficiency_data': efficiency_data,
        # Fleet
        'available_count': Vehicle.objects.filter(status='available').count(),
        'on_trip_count': on_trip_count,
        'in_shop_count': Vehicle.objects.filter(status='in_shop').count(),
        # Trip counts
        'trip_completed': total_trips,
        'trip_dispatched': Trip.objects.filter(status='dispatched').count(),
        'trip_draft': Trip.objects.filter(status='draft').count(),
        'trip_cancelled': Trip.objects.filter(status='cancelled').count(),
        # Table
        'vehicle_summary': vehicle_summary,
        'monthly_summary': monthly_summary,
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
        writer.writerow([v.name, fuel, maint, float(fuel)+float(maint), trips])
    return response