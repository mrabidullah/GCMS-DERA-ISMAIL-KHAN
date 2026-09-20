from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Event


def event_list(request):
    upcoming = Event.objects.filter(is_active=True, event_date__gte=timezone.now().date())
    past = Event.objects.filter(is_active=True, event_date__lt=timezone.now().date())
    return render(request, 'events/list.html', {
        'upcoming': upcoming,
        'past': past,
        'page_title': 'Events',
    })


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug, is_active=True)
    return render(request, 'events/detail.html', {
        'event': event,
        'page_title': event.title,
    })
