from django.contrib import admin
from .models import DownloadFile, DownloadCategory


@admin.register(DownloadCategory)
class DownloadCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    list_editable = ['order']


@admin.register(DownloadFile)
class DownloadFileAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'download_count', 'is_active', 'created_at']
    list_editable = ['is_active']
