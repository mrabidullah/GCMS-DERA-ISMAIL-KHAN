from django.contrib import admin
from .models import HeroSlide, PrincipalMessage, FeaturedVideo


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(PrincipalMessage)
class PrincipalMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'is_active']


@admin.register(FeaturedVideo)
class FeaturedVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_type', 'is_featured', 'is_active']
    list_editable = ['is_featured', 'is_active']
