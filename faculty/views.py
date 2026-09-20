from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import FacultyMember
from departments.models import Department


def faculty_list(request):
    query = request.GET.get('q', '')
    dept_slug = request.GET.get('dept', '')
    faculty = FacultyMember.objects.filter(is_active=True)
    departments = Department.objects.filter(is_active=True)

    if query:
        faculty = faculty.filter(
            Q(name__icontains=query) |
            Q(designation__icontains=query) |
            Q(specialization__icontains=query)
        )
    if dept_slug:
        faculty = faculty.filter(department__slug=dept_slug)

    return render(request, 'faculty/list.html', {
        'faculty': faculty,
        'departments': departments,
        'query': query,
        'dept_slug': dept_slug,
        'page_title': 'Faculty',
    })


def faculty_detail(request, slug):
    member = get_object_or_404(FacultyMember, slug=slug, is_active=True)
    return render(request, 'faculty/detail.html', {
        'member': member,
        'page_title': member.name,
    })
