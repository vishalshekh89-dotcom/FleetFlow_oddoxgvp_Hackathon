# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from vehicles.models import Vehicle
# from trips.models import Trip
# from drivers.models import Driver
# import datetime

# def get_group(user):
#     if user.is_superuser:
#         return 'Manager'
#     group = user.groups.first()
#     return group.name if group else ''

# @login_required
# def dashboard(request):
#     group = get_group(request.user)

#     # Redirect if not Manager
#     if group == 'Dispatcher':
#         return redirect('trip_list')
#     elif group == 'Safety Officer':
#         return redirect('driver_list')
#     elif group == 'Analyst':
#         return redirect('analytics')

#     total_vehicles = Vehicle.objects.count() or 1
#     available_count = Vehicle.objects.filter(status='available').count()
#     on_trip_count = Vehicle.objects.filter(status='on_trip').count()
#     in_shop_count = Vehicle.objects.filter(status='in_shop').count()
#     utilization_rate = round((on_trip_count / total_vehicles) * 100)
#     pending_trips = Trip.objects.filter(status='draft').count()
#     recent_trips = Trip.objects.order_by('-created_at')[:10]
#     expired_drivers = Driver.objects.filter(
#         license_expiry__lt=datetime.date.today()
#     )

#     context = {
#         'total_vehicles': total_vehicles,
#         'available_count': available_count,
#         'on_trip_count': on_trip_count,
#         'in_shop_count': in_shop_count,
#         'utilization_rate': utilization_rate,
#         'pending_trips': pending_trips,
#         'recent_trips': recent_trips,
#         'expired_drivers': expired_drivers,
#     }
#     return render(request, 'dashboard/dashboard.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from vehicles.models import Vehicle
from trips.models import Trip
from drivers.models import Driver
import datetime

def get_group(user):
    if user.is_superuser:
        return 'Manager'
    group = user.groups.first()
    return group.name if group else ''

@login_required
def dashboard(request):
    group = get_group(request.user)

    if group == 'Dispatcher':
        return redirect('trip_list')
    elif group == 'Safety Officer':
        return redirect('driver_list')
    elif group == 'Analyst':
        return redirect('analytics')

    total_vehicles = Vehicle.objects.count() or 1
    available_count = Vehicle.objects.filter(status='available').count()
    on_trip_count = Vehicle.objects.filter(status='on_trip').count()
    in_shop_count = Vehicle.objects.filter(status='in_shop').count()
    utilization_rate = round((on_trip_count / total_vehicles) * 100)
    pending_trips = Trip.objects.filter(status='draft').count()
    recent_trips = Trip.objects.order_by('-created_at')[:10]
    expired_drivers = Driver.objects.filter(
        license_expiry__lt=datetime.date.today()
    )

    context = {
        'total_vehicles': total_vehicles,
        'available_count': available_count,
        'on_trip_count': on_trip_count,
        'in_shop_count': in_shop_count,
        'utilization_rate': utilization_rate,
        'pending_trips': pending_trips,
        'recent_trips': recent_trips,
        'expired_drivers': expired_drivers,
    }
    return render(request, 'dashboard/dashboard.html', context)