from django.urls import path
from . import views

urlpatterns = [
    path('', views.admissions, name='admissions'),
    path('status/', views.admission_status, name='admission_status'),
    path('programs/', views.programs_list, name='programs'),
    path('programs/<slug:slug>/', views.program_detail, name='program_detail'),
]
