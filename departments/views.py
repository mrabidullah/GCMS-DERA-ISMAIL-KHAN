from django.shortcuts import render, get_object_or_404
from .models import Department
from faculty.models import FacultyMember
from admissions.models import AcademicProgram


def department_list(request):
    departments = Department.objects.filter(is_active=True)
    return render(request, 'departments/list.html', {
        'departments': departments,
        'page_title': 'Departments',
    })


def department_detail(request, slug):
    dept = get_object_or_404(Department, slug=slug, is_active=True)
    faculty = FacultyMember.objects.filter(department=dept, is_active=True)
    programs = AcademicProgram.objects.filter(department=dept, is_active=True)
    return render(request, 'departments/detail.html', {
        'dept': dept,
        'faculty': faculty,
        'programs': programs,
        'page_title': dept.name,
    })
