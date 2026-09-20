from django.contrib import admin

from .models import AcademicProgram, AdmissionApplication, AdmissionInfo


@admin.register(AcademicProgram)
class AcademicProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'department', 'duration', 'seats', 'is_active']
    list_filter = ['level', 'department']
    list_editable = ['is_active']


@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = ['application_number', 'applicant_name', 'program', 'status', 'merit_percentage', 'submitted_at']
    list_filter = ['status', 'program', 'preferred_department']
    search_fields = ['application_number', 'applicant_name', 'father_name', 'cnic_or_bform', 'phone']
    list_editable = ['status']
    readonly_fields = ['application_number', 'merit_percentage', 'submitted_at', 'reviewed_at']


@admin.register(AdmissionInfo)
class AdmissionInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'session', 'last_date', 'is_active']
    list_editable = ['is_active']
