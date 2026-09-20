from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentProfile, TeacherProfile, RegistrationRequest, LoginLog


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'get_full_name', 'user_type', 'is_approved', 'is_active', 'date_joined']
    list_filter = ['user_type', 'is_approved', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('GCMS Info', {'fields': ('user_type', 'is_approved', 'profile_picture', 'phone', 'address')}),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'roll_number', 'department', 'semester']
    list_filter = ['department']


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'designation', 'department', 'experience']
    list_filter = ['department']


@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'submitted_at']
    list_filter = ['status']
    actions = ['approve_users', 'reject_users']

    def approve_users(self, request, queryset):
        for req in queryset:
            req.status = 'approved'
            req.user.is_approved = True
            req.user.is_active = True
            req.user.save()
            req.save()
        self.message_user(request, f'{queryset.count()} user(s) approved.')
    approve_users.short_description = 'Approve selected registrations'

    def reject_users(self, request, queryset):
        queryset.update(status='rejected')
    reject_users.short_description = 'Reject selected registrations'


@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'login_time', 'ip_address']
    readonly_fields = ['user', 'login_time', 'ip_address', 'user_agent']
