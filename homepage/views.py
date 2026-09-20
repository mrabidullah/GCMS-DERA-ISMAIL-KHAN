from django.shortcuts import render
from .models import HeroSlide, PrincipalMessage, FeaturedVideo
from departments.models import Department
from faculty.models import FacultyMember
from news.models import NewsArticle
from announcements.models import Announcement
from admissions.models import AcademicProgram
from events.models import Event
from gallery.models import GalleryAlbum, GalleryItem
from core.models import QuickLink
from django.utils import timezone


def home(request):
    hero_slides = HeroSlide.objects.filter(is_active=True)
    principal_message = PrincipalMessage.objects.filter(is_active=True).first()
    featured_video = FeaturedVideo.objects.filter(is_featured=True, is_active=True).first()
    departments = Department.objects.filter(is_active=True)[:8]
    faculty_highlights = FacultyMember.objects.filter(is_active=True).order_by('-is_featured', 'order', 'name')[:6]
    latest_news = NewsArticle.objects.filter(status='published')[:6]
    announcements = Announcement.objects.filter(is_active=True).exclude(
        expiry_date__lt=timezone.now().date()
    )[:5]
    programs = AcademicProgram.objects.filter(is_active=True)[:6]
    upcoming_events = Event.objects.filter(
        is_active=True, event_date__gte=timezone.now().date()
    )[:4]
    gallery_albums = GalleryAlbum.objects.filter(is_active=True)[:6]
    quick_links = QuickLink.objects.filter(is_active=True)

    campus_facilities = [
        {'name': 'Library', 'icon': 'book'},
        {'name': 'Computer Lab', 'icon': 'desktop'},
        {'name': 'Sports Facilities', 'icon': 'futbol'},
        {'name': 'Cafeteria', 'icon': 'utensils'},
        {'name': 'Wi-Fi Campus', 'icon': 'wifi'},
        {'name': 'Transport', 'icon': 'bus'},
        {'name': 'Scholarship Program', 'icon': 'award'},
        {'name': 'Student Counseling', 'icon': 'hands-helping'},
    ]
    context = {
        'hero_slides': hero_slides,
        'principal_message': principal_message,
        'featured_video': featured_video,
        'departments': departments,
        'faculty_highlights': faculty_highlights,
        'latest_news': latest_news,
        'announcements': announcements,
        'programs': programs,
        'upcoming_events': upcoming_events,
        'gallery_albums': gallery_albums,
        'quick_links': quick_links,
        'campus_facilities': campus_facilities,
        'page_title': 'Home',
    }
    return render(request, 'homepage/home.html', context)


def about(request):
    return render(request, 'homepage/about.html', {'page_title': 'About GCMS'})


def principal_message(request):
    message = PrincipalMessage.objects.filter(is_active=True).first()
    return render(request, 'homepage/principal_message.html', {
        'message': message,
        'page_title': "Principal's Message"
    })


def privacy_policy(request):
    return render(request, 'homepage/privacy_policy.html', {'page_title': 'Privacy Policy'})


def terms_conditions(request):
    return render(request, 'homepage/terms_conditions.html', {'page_title': 'Terms & Conditions'})


def faq(request):
    from core.models import FAQ
    faqs = FAQ.objects.filter(is_active=True)
    return render(request, 'homepage/faq.html', {'faqs': faqs, 'page_title': 'FAQs'})
