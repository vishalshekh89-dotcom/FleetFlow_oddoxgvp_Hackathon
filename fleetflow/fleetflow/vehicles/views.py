# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import Vehicle

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
# def vehicle_list(request):
#     group = get_group(request.user)
#     if group not in ['Manager', 'Dispatcher']:
#         messages.error(request, 'Access Denied!')
#         return redirect_user(group)

#     vehicles = Vehicle.objects.all()
#     status = request.GET.get('status')
#     q = request.GET.get('q')
#     if status:
#         vehicles = vehicles.filter(status=status)
#     if q:
#         vehicles = vehicles.filter(name__icontains=q) | vehicles.filter(license_plate__icontains=q)
#     return render(request, 'vehicles/vehicle_list.html', {'vehicles': vehicles})

# @login_required
# def vehicle_add(request):
#     group = get_group(request.user)
#     if group not in ['Manager', 'Dispatcher']:
#         messages.error(request, 'Access Denied!')
#         return redirect_user(group)

#     if request.method == 'POST':
#         name = request.POST.get('name')
#         license_plate = request.POST.get('license_plate')
#         vehicle_type = request.POST.get('vehicle_type')
#         max_capacity_kg = request.POST.get('max_capacity_kg')
#         odometer = request.POST.get('odometer') or 0
#         region = request.POST.get('region', '')

#         if not all([name, license_plate, vehicle_type, max_capacity_kg]):
#             messages.error(request, 'Please fill all required fields.')
#             return render(request, 'vehicles/vehicle_form.html', {})

#         if Vehicle.objects.filter(license_plate=license_plate).exists():
#             messages.error(request, 'License plate already exists!')
#             return render(request, 'vehicles/vehicle_form.html', {})

#         Vehicle.objects.create(
#             name=name,
#             license_plate=license_plate,
#             vehicle_type=vehicle_type,
#             max_capacity_kg=max_capacity_kg,
#             odometer=odometer,
#             region=region,
#             status='available'
#         )
#         messages.success(request, f'{name} added successfully!')
#         return redirect('vehicle_list')

#     return render(request, 'vehicles/vehicle_form.html', {})

# @login_required
# def vehicle_edit(request, pk):
#     group = get_group(request.user)
#     if group not in ['Manager', 'Dispatcher']:
#         messages.error(request, 'Access Denied!')
#         return redirect_user(group)

#     vehicle = get_object_or_404(Vehicle, pk=pk)
#     if request.method == 'POST':
#         vehicle.name = request.POST.get('name')
#         vehicle.license_plate = request.POST.get('license_plate')
#         vehicle.vehicle_type = request.POST.get('vehicle_type')
#         vehicle.max_capacity_kg = request.POST.get('max_capacity_kg')
#         vehicle.odometer = request.POST.get('odometer') or 0
#         vehicle.region = request.POST.get('region', '')
#         vehicle.status = request.POST.get('status', vehicle.status)
#         vehicle.save()
#         messages.success(request, 'Vehicle updated!')
#         return redirect('vehicle_list')
#     return render(request, 'vehicles/vehicle_form.html', {'vehicle': vehicle})

# @login_required
# def vehicle_delete(request, pk):
#     group = get_group(request.user)
#     if group not in ['Manager']:
#         messages.error(request, 'Only Manager can retire vehicles!')
#         return redirect_user(group)

#     vehicle = get_object_or_404(Vehicle, pk=pk)
#     vehicle.status = 'retired'
#     vehicle.save()
#     messages.success(request, f'{vehicle.name} marked as Retired.')
#     return redirect('vehicle_list')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vehicle

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
def vehicle_list(request):
    group = get_group(request.user)
    if group not in ['Manager', 'Dispatcher']:
        messages.error(request, 'Access Denied!')
        return redirect_user(group)

    vehicles = Vehicle.objects.all()
    status = request.GET.get('status')
    q = request.GET.get('q')
    if status:
        vehicles = vehicles.filter(status=status)
    if q:
        vehicles = vehicles.filter(name__icontains=q) | vehicles.filter(license_plate__icontains=q)
    return render(request, 'vehicles/vehicle_list.html', {'vehicles': vehicles})

@login_required
def vehicle_add(request):
    group = get_group(request.user)
    if group not in ['Manager', 'Dispatcher']:
        messages.error(request, 'Access Denied!')
        return redirect_user(group)

    if request.method == 'POST':
        name = request.POST.get('name')
        license_plate = request.POST.get('license_plate')
        vehicle_type = request.POST.get('vehicle_type')
        max_capacity_kg = request.POST.get('max_capacity_kg')
        odometer = request.POST.get('odometer') or 0
        region = request.POST.get('region', '')

        if not all([name, license_plate, vehicle_type, max_capacity_kg]):
            messages.error(request, 'Please fill all required fields.')
            return render(request, 'vehicles/vehicle_form.html', {})

        if Vehicle.objects.filter(license_plate=license_plate).exists():
            messages.error(request, 'License plate already exists!')
            return render(request, 'vehicles/vehicle_form.html', {})

        Vehicle.objects.create(
            name=name,
            license_plate=license_plate,
            vehicle_type=vehicle_type,
            max_capacity_kg=max_capacity_kg,
            odometer=odometer,
            region=region,
            status='available'
        )
        messages.success(request, f'{name} added successfully!')
        return redirect('vehicle_list')

    return render(request, 'vehicles/vehicle_form.html', {})

@login_required
def vehicle_edit(request, pk):
    group = get_group(request.user)
    if group not in ['Manager', 'Dispatcher']:
        messages.error(request, 'Access Denied!')
        return redirect_user(group)

    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        vehicle.name = request.POST.get('name')
        vehicle.license_plate = request.POST.get('license_plate')
        vehicle.vehicle_type = request.POST.get('vehicle_type')
        vehicle.max_capacity_kg = request.POST.get('max_capacity_kg')
        vehicle.odometer = request.POST.get('odometer') or 0
        vehicle.region = request.POST.get('region', '')
        vehicle.status = request.POST.get('status', vehicle.status)
        vehicle.save()
        messages.success(request, 'Vehicle updated!')
        return redirect('vehicle_list')
    return render(request, 'vehicles/vehicle_form.html', {'vehicle': vehicle})

@login_required
def vehicle_delete(request, pk):
    group = get_group(request.user)
    if group not in ['Manager']:
        messages.error(request, 'Only Manager can retire vehicles!')
        return redirect_user(group)

    vehicle = get_object_or_404(Vehicle, pk=pk)
    vehicle.status = 'retired'
    vehicle.save()
    messages.success(request, f'{vehicle.name} marked as Retired.')
    return redirect('vehicle_list')