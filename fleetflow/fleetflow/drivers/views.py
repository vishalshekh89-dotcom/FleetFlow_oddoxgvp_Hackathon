# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import Driver
# import datetime

# @login_required
# def driver_list(request):
#     drivers = Driver.objects.all()
#     expired_drivers = Driver.objects.filter(license_expiry__lt=datetime.date.today())
#     return render(request, 'drivers/driver_list.html', {
#         'drivers': drivers,
#         'expired_drivers': expired_drivers,
#     })

# @login_required
# def driver_add(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         license_number = request.POST.get('license_number')
#         license_expiry = request.POST.get('license_expiry')
#         license_category = request.POST.get('license_category')
#         safety_score = request.POST.get('safety_score') or 100
#         status = request.POST.get('status', 'off_duty')

#         if not all([name, phone, license_number, license_expiry, license_category]):
#             messages.error(request, 'Please fill all required fields.')
#             return render(request, 'drivers/driver_form.html', {})

#         if Driver.objects.filter(license_number=license_number).exists():
#             messages.error(request, 'License number already exists!')
#             return render(request, 'drivers/driver_form.html', {})

#         Driver.objects.create(
#             name=name,
#             phone=phone,
#             license_number=license_number,
#             license_expiry=license_expiry,
#             license_category=license_category,
#             safety_score=safety_score,
#             status=status,
#         )
#         messages.success(request, f'{name} added successfully!')
#         return redirect('driver_list')

#     return render(request, 'drivers/driver_form.html', {})

# @login_required
# def driver_edit(request, pk):
#     driver = get_object_or_404(Driver, pk=pk)
#     if request.method == 'POST':
#         driver.name = request.POST.get('name')
#         driver.phone = request.POST.get('phone')
#         driver.license_number = request.POST.get('license_number')
#         driver.license_expiry = request.POST.get('license_expiry')
#         driver.license_category = request.POST.get('license_category')
#         driver.safety_score = request.POST.get('safety_score') or 100
#         driver.status = request.POST.get('status', driver.status)
#         driver.save()
#         messages.success(request, 'Driver updated!')
#         return redirect('driver_list')
#     return render(request, 'drivers/driver_form.html', {'driver': driver})

# @login_required
# def driver_delete(request, pk):
#     driver = get_object_or_404(Driver, pk=pk)
#     driver.delete()
#     messages.success(request, 'Driver removed.')
#     return redirect('driver_list')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Driver
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
def driver_list(request):
    group = get_group(request.user)
    if group not in ['Manager', 'Safety Officer']:
        messages.error(request, 'Access Denied!')
        return redirect_user(group)

    drivers = Driver.objects.all()
    expired_drivers = Driver.objects.filter(
        license_expiry__lt=datetime.date.today()
    )
    return render(request, 'drivers/driver_list.html', {
        'drivers': drivers,
        'expired_drivers': expired_drivers,
    })

@login_required
def driver_add(request):
    group = get_group(request.user)
    if group not in ['Manager', 'Safety Officer']:
        messages.error(request, 'Access Denied!')
        return redirect_user(group)

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        license_number = request.POST.get('license_number')
        license_expiry = request.POST.get('license_expiry')
        license_category = request.POST.get('license_category')
        safety_score = request.POST.get('safety_score') or 100
        status = request.POST.get('status', 'off_duty')

        if not all([name, phone, license_number, license_expiry, license_category]):
            messages.error(request, 'Please fill all required fields.')
            return render(request, 'drivers/driver_form.html', {})

        if Driver.objects.filter(license_number=license_number).exists():
            messages.error(request, 'License number already exists!')
            return render(request, 'drivers/driver_form.html', {})

        Driver.objects.create(
            name=name,
            phone=phone,
            license_number=license_number,
            license_expiry=license_expiry,
            license_category=license_category,
            safety_score=safety_score,
            status=status,
        )
        messages.success(request, f'{name} added successfully!')
        return redirect('driver_list')

    return render(request, 'drivers/driver_form.html', {})

@login_required
def driver_edit(request, pk):
    group = get_group(request.user)
    if group not in ['Manager', 'Safety Officer']:
        messages.error(request, 'Access Denied!')
        return redirect_user(group)

    driver = get_object_or_404(Driver, pk=pk)
    if request.method == 'POST':
        driver.name = request.POST.get('name')
        driver.phone = request.POST.get('phone')
        driver.license_number = request.POST.get('license_number')
        driver.license_expiry = request.POST.get('license_expiry')
        driver.license_category = request.POST.get('license_category')
        driver.safety_score = request.POST.get('safety_score') or 100
        driver.status = request.POST.get('status', driver.status)
        driver.save()
        messages.success(request, 'Driver updated!')
        return redirect('driver_list')
    return render(request, 'drivers/driver_form.html', {'driver': driver})

@login_required
def driver_delete(request, pk):
    group = get_group(request.user)
    if group not in ['Manager', 'Safety Officer']:
        messages.error(request, 'Access Denied!')
        return redirect_user(group)

    driver = get_object_or_404(Driver, pk=pk)
    driver.delete()
    messages.success(request, 'Driver removed.')
    return redirect('driver_list')