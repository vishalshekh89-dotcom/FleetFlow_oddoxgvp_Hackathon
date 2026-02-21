# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import FuelLog
# from maintenance.models import MaintenanceLog
# from vehicles.models import Vehicle
# from trips.models import Trip
# from django.db.models import Sum

# @login_required
# def expense_list(request):
#     fuel_logs = FuelLog.objects.all().order_by('-date')
#     total_fuel = FuelLog.objects.aggregate(t=Sum('cost'))['t'] or 0
#     total_maintenance = MaintenanceLog.objects.aggregate(t=Sum('cost'))['t'] or 0
#     total_operational = float(total_fuel) + float(total_maintenance)
#     return render(request, 'expenses/expense_list.html', {
#         'fuel_logs': fuel_logs,
#         'total_fuel': total_fuel,
#         'total_maintenance': total_maintenance,
#         'total_operational': total_operational,
#     })

# @login_required
# def fuel_add(request):
#     vehicles = Vehicle.objects.all()
#     trips = Trip.objects.filter(status__in=['dispatched', 'completed'])
#     if request.method == 'POST':
#         vehicle_id = request.POST.get('vehicle')
#         trip_id = request.POST.get('trip') or None
#         liters = request.POST.get('liters')
#         cost = request.POST.get('cost')
#         date = request.POST.get('date')

#         if not all([vehicle_id, liters, cost, date]):
#             messages.error(request, 'Please fill all required fields.')
#             return render(request, 'expenses/fuel_form.html', {'vehicles': vehicles, 'trips': trips})

#         FuelLog.objects.create(
#             vehicle=Vehicle.objects.get(pk=vehicle_id),
#             trip=Trip.objects.get(pk=trip_id) if trip_id else None,
#             liters=liters,
#             cost=cost,
#             date=date
#         )
#         messages.success(request, 'Fuel log added!')
#         return redirect('expense_list')

#     return render(request, 'expenses/fuel_form.html', {'vehicles': vehicles, 'trips': trips})


# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import FuelLog
# from maintenance.models import MaintenanceLog
# from vehicles.models import Vehicle
# from trips.models import Trip
# from django.db.models import Sum

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
#     elif group == 'Analyst':
#         return redirect('analytics')
#     return redirect('dashboard')

# @login_required
# def expense_list(request):
#     group = get_group(request.user)
#     if group not in ['Manager', 'Dispatcher']:
#         messages.error(request, 'Access Denied!')
#         return redirect_user(group)

#     fuel_logs = FuelLog.objects.all().order_by('-date')
#     total_fuel = FuelLog.objects.aggregate(t=Sum('cost'))['t'] or 0
#     total_maintenance = MaintenanceLog.objects.aggregate(t=Sum('cost'))['t'] or 0
#     total_operational = float(total_fuel) + float(total_maintenance)
#     return render(request, 'expenses/expense_list.html', {
#         'fuel_logs': fuel_logs,
#         'total_fuel': total_fuel,
#         'total_maintenance': total_maintenance,
#         'total_operational': total_operational,
#     })

# @login_required
# def fuel_add(request):
#     group = get_group(request.user)
#     if group not in ['Manager', 'Dispatcher']:
#         messages.error(request, 'Access Denied!')
#         return redirect_user(group)

#     vehicles = Vehicle.objects.all()
#     trips = Trip.objects.filter(status__in=['dispatched', 'completed'])
#     if request.method == 'POST':
#         vehicle_id = request.POST.get('vehicle')
#         trip_id = request.POST.get('trip') or None
#         liters = request.POST.get('liters')
#         cost = request.POST.get('cost')
#         date = request.POST.get('date')

#         if not all([vehicle_id, liters, cost, date]):
#             messages.error(request, 'Please fill all required fields.')
#             return render(request, 'expenses/fuel_form.html', {
#                 'vehicles': vehicles, 'trips': trips
#             })

#         FuelLog.objects.create(
#             vehicle=Vehicle.objects.get(pk=vehicle_id),
#             trip=Trip.objects.get(pk=trip_id) if trip_id else None,
#             liters=liters,
#             cost=cost,
#             date=date
#         )
#         messages.success(request, 'Fuel log added!')
#         return redirect('expense_list')

#     return render(request, 'expenses/fuel_form.html', {
#         'vehicles': vehicles, 'trips': trips
#     })




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FuelLog
from maintenance.models import MaintenanceLog
from vehicles.models import Vehicle
from trips.models import Trip
from django.db.models import Sum

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
    elif group == 'Analyst':
        return redirect('analytics')
    return redirect('dashboard')

@login_required
def expense_list(request):
    group = get_group(request.user)
    if group not in ['Manager', 'Dispatcher']:
        messages.error(request, 'Access Denied!')
        return redirect_user(group)

    fuel_logs = FuelLog.objects.all().order_by('-date')
    total_fuel = FuelLog.objects.aggregate(t=Sum('cost'))['t'] or 0
    total_maintenance = MaintenanceLog.objects.aggregate(t=Sum('cost'))['t'] or 0
    total_operational = float(total_fuel) + float(total_maintenance)
    return render(request, 'expenses/expense_list.html', {
        'fuel_logs': fuel_logs,
        'total_fuel': total_fuel,
        'total_maintenance': total_maintenance,
        'total_operational': total_operational,
    })

@login_required
def fuel_add(request):
    group = get_group(request.user)
    if group not in ['Manager', 'Dispatcher']:
        messages.error(request, 'Access Denied!')
        return redirect_user(group)

    vehicles = Vehicle.objects.all()
    trips = Trip.objects.filter(status__in=['dispatched', 'completed'])
    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle')
        trip_id = request.POST.get('trip') or None
        liters = request.POST.get('liters')
        cost = request.POST.get('cost')
        date = request.POST.get('date')

        if not all([vehicle_id, liters, cost, date]):
            messages.error(request, 'Please fill all required fields.')
            return render(request, 'expenses/fuel_form.html', {
                'vehicles': vehicles, 'trips': trips
            })

        FuelLog.objects.create(
            vehicle=Vehicle.objects.get(pk=vehicle_id),
            trip=Trip.objects.get(pk=trip_id) if trip_id else None,
            liters=liters,
            cost=cost,
            date=date
        )
        messages.success(request, 'Fuel log added!')
        return redirect('expense_list')

    return render(request, 'expenses/fuel_form.html', {
        'vehicles': vehicles, 'trips': trips
    })