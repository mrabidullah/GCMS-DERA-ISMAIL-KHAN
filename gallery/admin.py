from django.contrib import admin
from .models import GalleryAlbum, GalleryItem


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['album', 'item_type', 'title', 'order']
    list_filter = ['album', 'item_type']
