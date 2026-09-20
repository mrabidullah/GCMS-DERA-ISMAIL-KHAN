from django.db import models
from django.utils.text import slugify


class FacultyMember(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    photo = models.ImageField(upload_to='faculty/', blank=True, null=True)
    designation = models.CharField(max_length=200)
    qualification = models.CharField(max_length=300)
    department = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, null=True, blank=True)
    biography = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    office_hours = models.CharField(max_length=200, blank=True)
    specialization = models.CharField(max_length=300, blank=True)
    experience_years = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} – {self.designation}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            counter = 1
            while FacultyMember.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f'/faculty/{self.slug}/'
