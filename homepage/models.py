from django.db import models


class HeroSlide(models.Model):
    title = models.CharField(max_length=300)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    background_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    button_text = models.CharField(max_length=100, blank=True, default='Learn More')
    button_link = models.CharField(max_length=200, blank=True, default='#')
    button2_text = models.CharField(max_length=100, blank=True)
    button2_link = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class PrincipalMessage(models.Model):
    name = models.CharField(max_length=200, default='Principal')
    designation = models.CharField(max_length=200, default='Principal, GCMS D.I. Khan')
    photo = models.ImageField(upload_to='principal/', blank=True, null=True)
    message = models.TextField()
    qualification = models.CharField(max_length=300, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Principal's Message"
        verbose_name_plural = "Principal's Message"

    def __str__(self):
        return f"Message from {self.name}"


class FeaturedVideo(models.Model):
    VIDEO_TYPE_CHOICES = (
        ('youtube', 'YouTube'),
        ('facebook', 'Facebook'),
        ('mp4', 'Direct MP4'),
    )
    title = models.CharField(max_length=300)
    video_type = models.CharField(max_length=10, choices=VIDEO_TYPE_CHOICES, default='youtube')
    video_url = models.URLField(blank=True)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='videos/thumbs/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.title

    def get_embed_url(self):
        if self.video_type == 'youtube' and self.video_url:
            if 'watch?v=' in self.video_url:
                vid_id = self.video_url.split('watch?v=')[1].split('&')[0]
                return f'https://www.youtube.com/embed/{vid_id}'
            elif 'youtu.be/' in self.video_url:
                vid_id = self.video_url.split('youtu.be/')[1]
                return f'https://www.youtube.com/embed/{vid_id}'
        return self.video_url
