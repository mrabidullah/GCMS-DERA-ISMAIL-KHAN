from django.contrib import admin
from .models import PageSEO


@admin.register(PageSEO)
class PageSEOAdmin(admin.ModelAdmin):
    list_display = ['page_key', 'meta_title']
