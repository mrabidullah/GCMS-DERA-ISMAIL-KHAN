from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.crypto import get_random_string


class AcademicProgram(models.Model):
    LEVEL_CHOICES = (
        ('undergraduate', 'Undergraduate'),
        ('graduate', 'Graduate'),
        ('postgraduate', 'Postgraduate'),
        ('two_year', 'Two Year Program'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
        ('short_course', 'Short Course'),
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='undergraduate')
    department = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, null=True, blank=True)
    duration = models.CharField(max_length=50, blank=True, default='4 Years')
    description = models.TextField(blank=True)
    eligibility = models.TextField(blank=True)
    seats = models.IntegerField(default=0)
    fee_per_semester = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class AdmissionApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('waiting', 'Waiting'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
    )
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='admission_applications',
    )
    application_number = models.CharField(max_length=30, unique=True, blank=True)
    program = models.ForeignKey(AcademicProgram, on_delete=models.PROTECT, related_name='applications')
    preferred_department = models.ForeignKey(
        'departments.Department',
        on_delete=models.PROTECT,
        related_name='admission_applications',
        blank=True,
        null=True,
    )
    applicant_name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    cnic_or_bform = models.CharField(max_length=20, verbose_name='CNIC/B-Form')
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()
    photo = models.ImageField(upload_to='admissions/photos/', blank=True, null=True)
    previous_school = models.CharField(max_length=250, blank=True)
    board_or_university = models.CharField(max_length=200, blank=True)
    obtained_marks = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    total_marks = models.PositiveIntegerField(default=1100, validators=[MinValueValidator(1)])
    merit_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['status', '-submitted_at']),
            models.Index(fields=['program', 'status']),
            models.Index(fields=['cnic_or_bform']),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(obtained_marks__lte=models.F('total_marks')),
                name='admission_marks_not_above_total_v2',
            ),
        ]

    def __str__(self):
        return f"{self.application_number} - {self.applicant_name}"

    def save(self, *args, **kwargs):
        if self.total_marks:
            self.merit_percentage = round((self.obtained_marks / self.total_marks) * 100, 2)
        if not self.application_number:
            alphabet = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ'
            while True:
                candidate = f'GCMS-{get_random_string(4, alphabet)}-{get_random_string(4, alphabet)}'
                if not AdmissionApplication.objects.filter(application_number=candidate).exists():
                    self.application_number = candidate
                    break
        super().save(*args, **kwargs)


class AdmissionInfo(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    last_date = models.DateField(blank=True, null=True)
    session = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
