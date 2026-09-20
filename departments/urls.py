from django.urls import path
from . import views

urlpatterns = [
    path('', views.department_list, name='departments'),
    path('<slug:slug>/', views.department_detail, name='department_detail'),
]
