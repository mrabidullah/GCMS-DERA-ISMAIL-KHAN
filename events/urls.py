from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='events'),
    path('<slug:slug>/', views.event_detail, name='event_detail'),
]
