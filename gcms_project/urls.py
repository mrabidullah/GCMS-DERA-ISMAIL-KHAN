from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('accounts/', include('accounts.urls')),
    path('departments/', include('departments.urls')),
    path('faculty/', include('faculty.urls')),
    path('admissions/', include('admissions.urls')),
    path('news/', include('news.urls')),
    path('announcements/', include('announcements.urls')),
    path('gallery/', include('gallery.urls')),
    path('events/', include('events.urls')),
    path('downloads/', include('downloads.urls')),
    path('contact/', include('contact.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('search/', include('core.urls')),
    path('', include('seo.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'core.views.handler404'
