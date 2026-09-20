from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    is_approved = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.user_type})"

    def get_profile(self):
        if self.user_type == 'student':
            return getattr(self, 'student_profile', None)
        elif self.user_type == 'teacher':
            return getattr(self, 'teacher_profile', None)
        return None


class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=50, blank=True)
    registration_number = models.CharField(max_length=50, blank=True)
    father_name = models.CharField(max_length=200, blank=True)
    cnic = models.CharField(max_length=20, blank=True, verbose_name='CNIC/B-Form')
    department = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.CharField(max_length=20, blank=True)
    session = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Student: {self.user.get_full_name()}"


class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_profile')
    employee_id = models.CharField(max_length=50, blank=True)
    qualification = models.CharField(max_length=300, blank=True)
    designation = models.CharField(max_length=200, blank=True)
    department = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, null=True, blank=True)
    experience = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=300, blank=True)
    biography = models.TextField(blank=True)
    office_hours = models.CharField(max_length=200, blank=True)
    profile_changes_pending = models.BooleanField(default=False)

    def __str__(self):
        return f"Teacher: {self.user.get_full_name()}"


class RegistrationRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='registration_request')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    admin_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user} — {self.status}"


class LoginLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ['-login_time']

    def __str__(self):
        return f"{self.user} at {self.login_time}"
