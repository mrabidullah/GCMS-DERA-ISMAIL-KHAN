from django.shortcuts import render
from django.db.models import Q
from news.models import NewsArticle
from faculty.models import FacultyMember
from departments.models import Department
from admissions.models import AcademicProgram
from announcements.models import Announcement
from downloads.models import DownloadFile


def search_view(request):
    query = request.GET.get('q', '').strip()
    results = {}
    has_results = False
    if query:
        results['news'] = NewsArticle.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            status='published'
        )[:5]
        results['faculty'] = FacultyMember.objects.filter(
            Q(name__icontains=query) | Q(designation__icontains=query) | Q(biography__icontains=query),
            is_active=True
        )[:5]
        results['departments'] = Department.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            is_active=True
        )[:5]
        results['programs'] = AcademicProgram.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            is_active=True
        )[:5]
        results['announcements'] = Announcement.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            is_active=True
        )[:5]
        results['downloads'] = DownloadFile.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            is_active=True
        )[:5]
        has_results = any(items.exists() for items in results.values())
    return render(request, 'core/search.html', {'query': query, 'results': results, 'has_results': has_results})


def handler404(request, exception):
    return render(request, '404.html', status=404)
