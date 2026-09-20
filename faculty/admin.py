from django.contrib import admin
from .models import FacultyMember


@admin.register(FacultyMember)
class FacultyMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'department', 'is_featured', 'is_active']
    list_filter = ['department', 'is_featured', 'is_active']
    list_editable = ['is_featured', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
