from django.db import models
from django.utils import timezone


class Announcement(models.Model):
    PRIORITY_CHOICES = (
        ('normal', 'Normal'),
        ('important', 'Important'),
        ('urgent', 'Urgent'),
    )
    title = models.CharField(max_length=300)
    content = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    is_pinned = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    expiry_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title

    def is_expired(self):
        if self.expiry_date:
            return self.expiry_date < timezone.now().date()
        return False
