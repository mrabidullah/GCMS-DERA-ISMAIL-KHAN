from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Announcement


def announcement_list(request):
    announcements = Announcement.objects.filter(is_active=True).exclude(
        expiry_date__lt=timezone.now().date()
    )
    return render(request, 'announcements/list.html', {
        'announcements': announcements,
        'page_title': 'Announcements',
    })
