from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status']
    list_editable = ['status']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'ip_address', 'created_at']
