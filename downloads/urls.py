from django.urls import path
from . import views

urlpatterns = [
    path('', views.downloads_list, name='downloads'),
    path('download/<int:pk>/', views.download_file, name='download_file'),
]
