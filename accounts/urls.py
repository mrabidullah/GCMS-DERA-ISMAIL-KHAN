from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('registration-submitted/', views.registration_submitted, name='registration_submitted'),
    path('student-portal/', views.student_portal, name='student_portal'),
    path('teacher-portal/', views.teacher_portal, name='teacher_portal'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
]
