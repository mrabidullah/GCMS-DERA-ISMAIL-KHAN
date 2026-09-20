from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'location', 'is_featured', 'is_active']
    list_editable = ['is_featured', 'is_active']
