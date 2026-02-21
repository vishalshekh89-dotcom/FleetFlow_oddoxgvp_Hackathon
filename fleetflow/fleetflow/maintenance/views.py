# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import MaintenanceLog
# from vehicles.models import Vehicle

# @login_required
# def maintenance_list(request):
#     logs = MaintenanceLog.objects.all().order_by('-date')
#     return render(request, 'maintenance/maintenance_list.html', {'logs': logs})

# @login_required
# def maintenance_add(request):
#     vehicles = Vehicle.objects.all()
#     if request.method == 'POST':
#         vehicle_id = request.POST.get('vehicle')
#         description = request.POST.get('description')
#         cost = request.POST.get('cost')
#         date = request.POST.get('date')

#         if not all([vehicle_id, description, cost, date]):
#             messages.error(request, 'Please fill all fields.')
#             return render(request, 'maintenance/maintenance_form.html', {'vehicles': vehicles})

#         vehicle = Vehicle.objects.get(pk=vehicle_id)
#         MaintenanceLog.objects.create(
#             vehicle=vehicle,
#             description=description,
#             cost=cost,
#             date=date
#         )
#         messages.success(request, f'Maintenance logged! {vehicle.name} is now In Shop.')
#         return redirect('maintenance_list')

#     return render(request, 'maintenance/maintenance_form.html', {'vehicles': vehicles})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MaintenanceLog
from vehicles.models import Vehicle

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
def maintenance_list(request):
    group = get_group(request.user)
    if group not in ['Manager', 'Dispatcher']:
        messages.error(request, 'Access Denied!')
        return redirect_user(group)

    logs = MaintenanceLog.objects.all().order_by('-date')
    return render(request, 'maintenance/maintenance_list.html', {'logs': logs})

@login_required
def maintenance_add(request):
    group = get_group(request.user)
    if group not in ['Manager', 'Dispatcher']:
        messages.error(request, 'Access Denied!')
        return redirect_user(group)

    vehicles = Vehicle.objects.all()
    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle')
        description = request.POST.get('description')
        cost = request.POST.get('cost')
        date = request.POST.get('date')

        if not all([vehicle_id, description, cost, date]):
            messages.error(request, 'Please fill all fields.')
            return render(request, 'maintenance/maintenance_form.html', {'vehicles': vehicles})

        vehicle = Vehicle.objects.get(pk=vehicle_id)
        MaintenanceLog.objects.create(
            vehicle=vehicle,
            description=description,
            cost=cost,
            date=date
        )
        messages.success(request, f'Maintenance logged! {vehicle.name} is now In Shop.')
        return redirect('maintenance_list')

    return render(request, 'maintenance/maintenance_form.html', {'vehicles': vehicles})