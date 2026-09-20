from django.db import models


class PageSEO(models.Model):
    page_key = models.CharField(max_length=100, unique=True, help_text="e.g. home, about, contact")
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=300, blank=True)
    meta_keywords = models.TextField(blank=True)
    og_image = models.ImageField(upload_to='seo/', blank=True, null=True)
    canonical_url = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Page SEO'
        verbose_name_plural = 'Page SEO Settings'

    def __str__(self):
        return f"SEO: {self.page_key}"

    @classmethod
    def get_for_page(cls, key):
        obj, _ = cls.objects.get_or_create(page_key=key)
        return obj
