from django.db import models


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200, default="GCMS Dera Ismail Khan")
    site_tagline = models.CharField(max_length=300, default="Government College of Management Sciences")
    site_logo = models.ImageField(upload_to='site/', blank=True, null=True)
    site_favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_phone2 = models.CharField(max_length=20, blank=True)
    contact_address = models.TextField(blank=True)
    office_hours = models.CharField(max_length=200, blank=True, default="Mon–Fri: 8:00 AM – 4:00 PM")
    google_map_embed = models.TextField(blank=True, help_text="Google Maps embed iframe HTML")
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    footer_text = models.TextField(blank=True)
    established_year = models.IntegerField(default=1990)
    is_admission_open = models.BooleanField(default=False)
    admission_banner_text = models.CharField(max_length=300, blank=True)
    admission_link = models.CharField(max_length=200, blank=True, default='/admissions/')

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class QuickLink(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, blank=True, help_text="CSS icon class")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question
