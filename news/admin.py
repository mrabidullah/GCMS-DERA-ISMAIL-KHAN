from django.contrib import admin
from .models import NewsArticle, NewsCategory


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'is_featured', 'published_at']
    list_filter = ['status', 'category', 'is_featured']
    list_editable = ['status', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
