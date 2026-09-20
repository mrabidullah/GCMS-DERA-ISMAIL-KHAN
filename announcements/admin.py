from django.contrib import admin
from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'is_pinned', 'is_active', 'expiry_date', 'created_at']
    list_editable = ['priority', 'is_pinned', 'is_active']
