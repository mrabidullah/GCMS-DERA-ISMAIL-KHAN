from django.urls import path
from . import views

urlpatterns = [
    path('', views.faculty_list, name='faculty'),
    path('<slug:slug>/', views.faculty_detail, name='faculty_detail'),
]
