from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import RegistrationRequest

@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'username', 'requested_role', 'status', 'created_at']
    list_filter = ['status', 'requested_role']
    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        for reg in queryset.filter(status='pending'):
            # User બનાવો
            user = User.objects.create_user(
                username=reg.username,
                email=reg.email,
                password=reg.password,
            )
            user.first_name = reg.full_name
            user.save()

            # Group assign કરો
            try:
                group = Group.objects.get(name=reg.requested_role)
                user.groups.add(group)
            except Group.DoesNotExist:
                pass

            # Status update
            reg.status = 'approved'
            reg.reviewed_at = timezone.now()
            reg.save()

            # User ને email
            send_mail(
                subject='✅ FleetFlow — Account Approved!',
                message=f"""
Hello {reg.full_name},

Your FleetFlow account has been approved!

Login Details:
Username: {reg.username}
Role: {reg.requested_role}

Login here: http://127.0.0.1:8000/accounts/login/

Welcome to FleetFlow!
— FleetFlow Team
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[reg.email],
                fail_silently=False,
            )

        self.message_user(request, f'{queryset.count()} request(s) approved!', messages.SUCCESS)

    approve_requests.short_description = '✅ Approve Selected Requests'

    def reject_requests(self, request, queryset):
        for reg in queryset.filter(status='pending'):
            reg.status = 'rejected'
            reg.reviewed_at = timezone.now()
            reg.save()

            # User ને rejection email
            send_mail(
                subject='❌ FleetFlow — Registration Update',
                message=f"""
Hello {reg.full_name},

Unfortunately your FleetFlow registration request has been rejected.

If you think this is a mistake, please contact your administrator.

— FleetFlow Team
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[reg.email],
                fail_silently=False,
            )

        self.message_user(request, f'{queryset.count()} request(s) rejected!', messages.WARNING)

    reject_requests.short_description = '❌ Reject Selected Requests'