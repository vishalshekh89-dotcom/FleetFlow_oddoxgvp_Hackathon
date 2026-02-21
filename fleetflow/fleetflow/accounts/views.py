# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages

# def get_group(user):
#     if user.is_superuser:
#         return 'Manager'
#     group = user.groups.first()
#     return group.name if group else ''

# def redirect_by_group(group):
#     if group == 'Manager':
#         return redirect('dashboard')
#     elif group == 'Dispatcher':
#         return redirect('trip_list')
#     elif group == 'Safety Officer':
#         return redirect('driver_list')
#     elif group == 'Analyst':
#         return redirect('analytics')
#     else:
#         return redirect('dashboard')

# def login_view(request):
#     if request.user.is_authenticated:
#         group = get_group(request.user)
#         return redirect_by_group(group)

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             group = get_group(user)
#             return redirect_by_group(group)
#         else:
#             messages.error(request, 'Invalid username or password.')

#     return render(request, 'accounts/login.html')

# def logout_view(request):
#     logout(request)
#     return redirect('login')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import RegistrationRequest

def get_group(user):
    if user.is_superuser:
        return 'Manager'
    group = user.groups.first()
    return group.name if group else ''

def redirect_by_group(group):
    if group == 'Manager':
        return redirect('dashboard')
    elif group == 'Dispatcher':
        return redirect('trip_list')
    elif group == 'Safety Officer':
        return redirect('driver_list')
    elif group == 'Analyst':
        return redirect('analytics')
    return redirect('dashboard')

def login_view(request):
    if request.user.is_authenticated:
        group = get_group(request.user)
        return redirect_by_group(group)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            group = get_group(user)
            return redirect_by_group(group)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        requested_role = request.POST.get('requested_role')

        # Validations
        if not all([full_name, email, username, password, requested_role]):
            messages.error(request, 'Please fill all fields.')
            return render(request, 'accounts/register.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'accounts/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
            return render(request, 'accounts/register.html')

        if User.objects.filter(email=email).exists() or RegistrationRequest.objects.filter(email=email, status='pending').exists():
            messages.error(request, 'Email already registered or pending!')
            return render(request, 'accounts/register.html')

        # Request save કરો
        RegistrationRequest.objects.create(
            full_name=full_name,
            email=email,
            username=username,
            password=password,
            requested_role=requested_role,
        )

        # Superuser ને email
        superuser_emails = list(
            User.objects.filter(is_superuser=True).values_list('email', flat=True)
        )
        if superuser_emails:
            send_mail(
                subject='🔔 FleetFlow — New Registration Request',
                message=f"""
New registration request received!

Name: {full_name}
Email: {email}
Username: {username}
Requested Role: {requested_role}

Please review and approve/reject:
http://127.0.0.1:8000/admin/accounts/registrationrequest/

— FleetFlow System
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=superuser_emails,
                fail_silently=False,
            )

        return redirect('pending_approval')

    return render(request, 'accounts/register.html')

def pending_approval_view(request):
    return render(request, 'accounts/pending_approval.html')