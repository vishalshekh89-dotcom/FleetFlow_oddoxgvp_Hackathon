# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import Trip
# from vehicles.models import Vehicle
# from drivers.models import Driver
# import datetime

# @login_required
# def trip_list(request):
#     trips = Trip.objects.all().order_by('-created_at')
#     status = request.GET.get('status')
#     if status:
#         trips = trips.filter(status=status)
#     return render(request, 'trips/trip_list.html', {'trips': trips})

# @login_required
# def trip_add(request):
#     available_vehicles = Vehicle.objects.filter(status='available')
#     available_drivers = Driver.objects.filter(
#         status__in=['on_duty', 'off_duty'],
#         license_expiry__gte=datetime.date.today()
#     )
#     if request.method == 'POST':
#         vehicle_id = request.POST.get('vehicle')
#         driver_id = request.POST.get('driver')
#         cargo_weight_kg = float(request.POST.get('cargo_weight_kg') or 0)
#         origin = request.POST.get('origin')
#         destination = request.POST.get('destination')
#         start_odometer = request.POST.get('start_odometer')
#         notes = request.POST.get('notes', '')
#         action = request.POST.get('action', 'draft')

#         if not all([vehicle_id, driver_id, origin, destination, start_odometer]):
#             messages.error(request, 'Please fill all required fields.')
#             return render(request, 'trips/trip_form.html', {
#                 'available_vehicles': available_vehicles,
#                 'available_drivers': available_drivers,
#             })

#         vehicle = Vehicle.objects.get(pk=vehicle_id)
#         driver = Driver.objects.get(pk=driver_id)

#         # Cargo validation
#         if cargo_weight_kg > vehicle.max_capacity_kg:
#             messages.error(request, f'Cargo ({cargo_weight_kg}kg) exceeds vehicle capacity ({vehicle.max_capacity_kg}kg)!')
#             return render(request, 'trips/trip_form.html', {
#                 'available_vehicles': available_vehicles,
#                 'available_drivers': available_drivers,
#             })

#         trip = Trip.objects.create(
#             vehicle=vehicle,
#             driver=driver,
#             cargo_weight_kg=cargo_weight_kg,
#             origin=origin,
#             destination=destination,
#             start_odometer=start_odometer,
#             notes=notes,
#             status='draft'
#         )

#         if action == 'dispatch':
#             trip.status = 'dispatched'
#             trip.save()
#             vehicle.status = 'on_trip'
#             vehicle.save()
#             driver.status = 'on_duty'
#             driver.save()
#             messages.success(request, f'Trip #{trip.id} dispatched successfully!')
#         else:
#             messages.success(request, f'Trip #{trip.id} saved as draft.')

#         return redirect('trip_list')

#     return render(request, 'trips/trip_form.html', {
#         'available_vehicles': available_vehicles,
#         'available_drivers': available_drivers,
#     })

# @login_required
# def trip_edit(request, pk):
#     trip = get_object_or_404(Trip, pk=pk)
#     available_vehicles = Vehicle.objects.filter(status='available')
#     available_drivers = Driver.objects.filter(
#         status__in=['on_duty', 'off_duty'],
#         license_expiry__gte=datetime.date.today()
#     )
#     if request.method == 'POST':
#         trip.origin = request.POST.get('origin')
#         trip.destination = request.POST.get('destination')
#         trip.cargo_weight_kg = request.POST.get('cargo_weight_kg')
#         trip.notes = request.POST.get('notes', '')
#         trip.save()
#         messages.success(request, 'Trip updated!')
#         return redirect('trip_list')
#     return render(request, 'trips/trip_form.html', {
#         'trip': trip,
#         'available_vehicles': available_vehicles,
#         'available_drivers': available_drivers,
#     })

# @login_required
# def trip_dispatch(request, pk):
#     trip = get_object_or_404(Trip, pk=pk)
#     trip.status = 'dispatched'
#     trip.vehicle.status = 'on_trip'
#     trip.vehicle.save()
#     trip.driver.status = 'on_duty'
#     trip.driver.save()
#     trip.save()
#     messages.success(request, f'Trip #{trip.id} dispatched!')
#     return redirect('trip_list')

# @login_required
# def trip_complete(request, pk):
#     trip = get_object_or_404(Trip, pk=pk)
#     if request.method == 'POST':
#         end_odometer = request.POST.get('end_odometer')
#         if end_odometer:
#             trip.end_odometer = float(end_odometer)
#         trip.status = 'completed'
#         trip.vehicle.status = 'available'
#         trip.vehicle.save()
#         trip.driver.status = 'off_duty'
#         trip.driver.save()
#         trip.save()
#         messages.success(request, f'Trip #{trip.id} completed!')
#         return redirect('trip_list')
#     return render(request, 'trips/trip_complete.html', {'trip': trip})


# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import Trip
# from vehicles.models import Vehicle
# from drivers.models import Driver
# import datetime

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
# def trip_list(request):
#     group = get_group(request.user)
#     if group not in ['Manager', 'Dispatcher']:
#         messages.error(request, 'Access Denied!')
#         return redirect_user(group)

#     trips = Trip.objects.all().order_by('-created_at')
#     status = request.GET.get('status')
#     if status:
#         trips = trips.filter(status=status)
#     return render(request, 'trips/trip_list.html', {'trips': trips})

# @login_required
# def trip_add(request):
#     group = get_group(request.user)
#     if group not in ['Manager', 'Dispatcher']:
#         messages.error(request, 'Access Denied!')
#         return redirect_user(group)

#     available_vehicles = Vehicle.objects.filter(status='available')
#     available_drivers = Driver.objects.filter(
#         status__in=['on_duty', 'off_duty'],
#         license_expiry__gte=datetime.date.today()
#     )

#     if request.method == 'POST':
#         vehicle_id = request.POST.get('vehicle')
#         driver_id = request.POST.get('driver')
#         cargo_weight_kg = float(request.POST.get('cargo_weight_kg') or 0)
#         origin = request.POST.get('origin')
#         destination = request.POST.get('destination')
#         start_odometer = request.POST.get('start_odometer')
#         notes = request.POST.get('notes', '')
#         action = request.POST.get('action', 'draft')

#         if not all([vehicle_id, driver_id, origin, destination, start_odometer]):
#             messages.error(request, 'Please fill all required fields.')
#             return render(request, 'trips/trip_form.html', {
#                 'available_vehicles': available_vehicles,
#                 'available_drivers': available_drivers,
#             })

#         vehicle = Vehicle.objects.get(pk=vehicle_id)
#         driver = Driver.objects.get(pk=driver_id)

#         if cargo_weight_kg > vehicle.max_capacity_kg:
#             messages.error(request, f'Cargo ({cargo_weight_kg}kg) exceeds vehicle capacity ({vehicle.max_capacity_kg}kg)!')
#             return render(request, 'trips/trip_form.html', {
#                 'available_vehicles': available_vehicles,
#                 'available_drivers': available_drivers,
#             })

#         trip = Trip.objects.create(
#             vehicle=vehicle,
#             driver=driver,
#             cargo_weight_kg=cargo_weight_kg,
#             origin=origin,
#             destination=destination,
#             start_odometer=start_odometer,
#             notes=notes,
#             status='draft'
#         )

#         if action == 'dispatch':
#             trip.status = 'dispatched'
#             trip.save()
#             vehicle.status = 'on_trip'
#             vehicle.save()
#             driver.status = 'on_duty'
#             driver.save()
#             messages.success(request, f'Trip #{trip.id} dispatched!')
#         else:
#             messages.success(request, f'Trip #{trip.id} saved as draft.')

#         return redirect('trip_list')

#     return render(request, 'trips/trip_form.html', {
#         'available_vehicles': available_vehicles,
#         'available_drivers': available_drivers,
#     })

# @login_required
# def trip_edit(request, pk):
#     group = get_group(request.user)
#     if group not in ['Manager', 'Dispatcher']:
#         messages.error(request, 'Access Denied!')
#         return redirect_user(group)

#     trip = get_object_or_404(Trip, pk=pk)
#     available_vehicles = Vehicle.objects.filter(status='available')
#     available_drivers = Driver.objects.filter(
#         status__in=['on_duty', 'off_duty'],
#         license_expiry__gte=datetime.date.today()
#     )
#     if request.method == 'POST':
#         trip.origin = request.POST.get('origin')
#         trip.destination = request.POST.get('destination')
#         trip.cargo_weight_kg = request.POST.get('cargo_weight_kg')
#         trip.notes = request.POST.get('notes', '')
#         trip.save()
#         messages.success(request, 'Trip updated!')
#         return redirect('trip_list')
#     return render(request, 'trips/trip_form.html', {
#         'trip': trip,
#         'available_vehicles': available_vehicles,
#         'available_drivers': available_drivers,
#     })

# @login_required
# def trip_dispatch(request, pk):
#     group = get_group(request.user)
#     if group not in ['Manager', 'Dispatcher']:
#         messages.error(request, 'Access Denied!')
#         return redirect_user(group)

#     trip = get_object_or_404(Trip, pk=pk)
#     trip.status = 'dispatched'
#     trip.vehicle.status = 'on_trip'
#     trip.vehicle.save()
#     trip.driver.status = 'on_duty'
#     trip.driver.save()
#     trip.save()
#     messages.success(request, f'Trip #{trip.id} dispatched!')
#     return redirect('trip_list')

# @login_required
# def trip_complete(request, pk):
#     group = get_group(request.user)
#     if group not in ['Manager', 'Dispatcher']:
#         messages.error(request, 'Access Denied!')
#         return redirect_user(group)

#     trip = get_object_or_404(Trip, pk=pk)
#     if request.method == 'POST':
#         end_odometer = request.POST.get('end_odometer')
#         if end_odometer:
#             trip.end_odometer = float(end_odometer)
#         trip.status = 'completed'
#         trip.vehicle.status = 'available'
#         trip.vehicle.save()
#         trip.driver.status = 'off_duty'
#         trip.driver.save()
#         trip.save()
#         messages.success(request, f'Trip #{trip.id} completed!')
#         return redirect('trip_list')
#     return render(request, 'trips/trip_complete.html', {'trip': trip})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Trip
from vehicles.models import Vehicle
from drivers.models import Driver
import datetime

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
def trip_list(request):
    group = get_group(request.user)
    if group not in ['Manager', 'Dispatcher']:
        messages.error(request, 'Access Denied!')
        return redirect_user(group)

    trips = Trip.objects.all().order_by('-created_at')
    status = request.GET.get('status')
    if status:
        trips = trips.filter(status=status)
    return render(request, 'trips/trip_list.html', {'trips': trips})

@login_required
def trip_add(request):
    group = get_group(request.user)
    if group not in ['Manager', 'Dispatcher']:
        messages.error(request, 'Access Denied!')
        return redirect_user(group)

    available_vehicles = Vehicle.objects.filter(status='available')
    available_drivers = Driver.objects.filter(
        status__in=['on_duty', 'off_duty'],
        license_expiry__gte=datetime.date.today()
    )

    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle')
        driver_id = request.POST.get('driver')
        cargo_weight_kg = float(request.POST.get('cargo_weight_kg') or 0)
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        start_odometer = request.POST.get('start_odometer')
        notes = request.POST.get('notes', '')
        action = request.POST.get('action', 'draft')

        if not all([vehicle_id, driver_id, origin, destination, start_odometer]):
            messages.error(request, 'Please fill all required fields.')
            return render(request, 'trips/trip_form.html', {
                'available_vehicles': available_vehicles,
                'available_drivers': available_drivers,
            })

        vehicle = Vehicle.objects.get(pk=vehicle_id)
        driver = Driver.objects.get(pk=driver_id)

        if cargo_weight_kg > vehicle.max_capacity_kg:
            messages.error(request, f'Cargo ({cargo_weight_kg}kg) exceeds vehicle capacity ({vehicle.max_capacity_kg}kg)!')
            return render(request, 'trips/trip_form.html', {
                'available_vehicles': available_vehicles,
                'available_drivers': available_drivers,
            })

        trip = Trip.objects.create(
            vehicle=vehicle,
            driver=driver,
            cargo_weight_kg=cargo_weight_kg,
            origin=origin,
            destination=destination,
            start_odometer=start_odometer,
            notes=notes,
            status='draft'
        )

        if action == 'dispatch':
            trip.status = 'dispatched'
            trip.save()
            vehicle.status = 'on_trip'
            vehicle.save()
            driver.status = 'on_duty'
            driver.save()
            messages.success(request, f'Trip #{trip.id} dispatched!')
        else:
            messages.success(request, f'Trip #{trip.id} saved as draft.')

        return redirect('trip_list')

    return render(request, 'trips/trip_form.html', {
        'available_vehicles': available_vehicles,
        'available_drivers': available_drivers,
    })

@login_required
def trip_edit(request, pk):
    group = get_group(request.user)
    if group not in ['Manager', 'Dispatcher']:
        messages.error(request, 'Access Denied!')
        return redirect_user(group)

    trip = get_object_or_404(Trip, pk=pk)
    available_vehicles = Vehicle.objects.filter(status='available')
    available_drivers = Driver.objects.filter(
        status__in=['on_duty', 'off_duty'],
        license_expiry__gte=datetime.date.today()
    )
    if request.method == 'POST':
        trip.origin = request.POST.get('origin')
        trip.destination = request.POST.get('destination')
        trip.cargo_weight_kg = request.POST.get('cargo_weight_kg')
        trip.notes = request.POST.get('notes', '')
        trip.save()
        messages.success(request, 'Trip updated!')
        return redirect('trip_list')
    return render(request, 'trips/trip_form.html', {
        'trip': trip,
        'available_vehicles': available_vehicles,
        'available_drivers': available_drivers,
    })

@login_required
def trip_dispatch(request, pk):
    group = get_group(request.user)
    if group not in ['Manager', 'Dispatcher']:
        messages.error(request, 'Access Denied!')
        return redirect_user(group)

    trip = get_object_or_404(Trip, pk=pk)
    trip.status = 'dispatched'
    trip.vehicle.status = 'on_trip'
    trip.vehicle.save()
    trip.driver.status = 'on_duty'
    trip.driver.save()
    trip.save()
    messages.success(request, f'Trip #{trip.id} dispatched!')
    return redirect('trip_list')

@login_required
def trip_complete(request, pk):
    group = get_group(request.user)
    if group not in ['Manager', 'Dispatcher']:
        messages.error(request, 'Access Denied!')
        return redirect_user(group)

    trip = get_object_or_404(Trip, pk=pk)
    if request.method == 'POST':
        end_odometer = request.POST.get('end_odometer')
        if end_odometer:
            trip.end_odometer = float(end_odometer)
        trip.status = 'completed'
        trip.vehicle.status = 'available'
        trip.vehicle.save()
        trip.driver.status = 'off_duty'
        trip.driver.save()
        trip.save()
        messages.success(request, f'Trip #{trip.id} completed!')
        return redirect('trip_list')
    return render(request, 'trips/trip_complete.html', {'trip': trip})