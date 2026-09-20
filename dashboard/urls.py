from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('hero/', views.manage_hero, name='manage_hero'),
    path('news/', views.manage_news, name='manage_news'),
    path('announcements/', views.manage_announcements, name='manage_announcements'),
    path('faculty/', views.manage_faculty, name='manage_faculty'),
    path('admissions/', views.manage_admissions, name='manage_admissions'),
    path('registrations/', views.manage_registrations, name='manage_registrations'),
    path('settings/', views.manage_site_settings, name='manage_site_settings'),
    path('departments/', views.manage_departments, name='manage_departments'),
    path('gallery/', views.manage_gallery, name='manage_gallery'),
    path('events/', views.manage_events, name='manage_events'),
    path('downloads/', views.manage_downloads, name='manage_downloads'),
    path('messages/', views.manage_messages, name='manage_messages'),
    path('principal-message/', views.manage_principal_message, name='manage_principal_message'),
    path('video/', views.manage_video, name='manage_video'),
]
