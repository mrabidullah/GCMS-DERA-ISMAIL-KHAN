from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.http import urlencode

from departments.models import Department

from .models import AcademicProgram, AdmissionApplication, AdmissionInfo


def admissions(request):
    info = AdmissionInfo.objects.filter(is_active=True).first()
    programs = AcademicProgram.objects.filter(is_active=True)
    form_programs = programs.filter(
        Q(level__in=['two_year', 'diploma', 'certificate', 'short_course']) |
        Q(duration__icontains='2')
    )
    departments = Department.objects.filter(is_active=True)

    if request.method == 'POST':
        program_id = request.POST.get('program')
        department_id = request.POST.get('preferred_department')
        program = form_programs.filter(pk=program_id).first() if program_id else None
        department = Department.objects.filter(pk=department_id).first() if department_id else None
        if not program:
            messages.error(request, 'Please select a valid program.')
            return redirect('admissions')
        try:
            application = AdmissionApplication(
                user=request.user if request.user.is_authenticated else None,
                program=program,
                preferred_department=department,
                applicant_name=request.POST.get('applicant_name', '').strip(),
                father_name=request.POST.get('father_name', '').strip(),
                date_of_birth=request.POST.get('date_of_birth') or None,
                gender=request.POST.get('gender', ''),
                cnic_or_bform=request.POST.get('cnic_or_bform', '').strip(),
                phone=request.POST.get('phone', '').strip(),
                email=request.POST.get('email', '').strip(),
                address=request.POST.get('address', '').strip(),
                previous_school=request.POST.get('previous_school', '').strip(),
                board_or_university=request.POST.get('board_or_university', '').strip(),
                obtained_marks=int(request.POST.get('obtained_marks') or 0),
                total_marks=int(request.POST.get('total_marks') or 1100),
            )
        except ValueError:
            messages.error(request, 'Please enter valid marks.')
            return redirect('admissions')

        if not application.applicant_name or not application.father_name or not application.cnic_or_bform:
            messages.error(request, 'Please fill all required applicant fields.')
            return redirect('admissions')
        if application.obtained_marks > application.total_marks:
            messages.error(request, 'Obtained marks cannot be greater than total marks.')
            return redirect('admissions')
        if 'photo' in request.FILES:
            application.photo = request.FILES['photo']
        application.save()
        messages.success(request, f'Application submitted. Your application number is {application.application_number}.')
        query = urlencode({'application': application.application_number})
        return redirect(f"{reverse('admissions')}?{query}")

    application = None
    application_number = request.GET.get('application')
    if application_number:
        application = AdmissionApplication.objects.filter(
            application_number__iexact=application_number.strip(),
        ).select_related('program', 'preferred_department', 'user').first()

    return render(request, 'admissions/admissions.html', {
        'info': info,
        'programs': programs,
        'form_programs': form_programs,
        'departments': departments,
        'application': application,
        'page_title': 'Admissions',
    })


def programs_list(request):
    programs = AcademicProgram.objects.filter(is_active=True)
    return render(request, 'admissions/programs.html', {
        'programs': programs,
        'page_title': 'Academic Programs',
    })


def program_detail(request, slug):
    program = get_object_or_404(AcademicProgram, slug=slug, is_active=True)
    return render(request, 'admissions/program_detail.html', {
        'program': program,
        'page_title': program.name,
    })


def admission_status(request):
    application = None
    if request.method == 'POST':
        application_number = request.POST.get('application_number', '').strip()
        if application_number:
            query = urlencode({'application_number': application_number})
            return redirect(f"{reverse('admission_status')}?{query}")
        messages.error(request, 'Please enter your GCMS application number.')
    elif request.GET.get('application_number'):
        application_number = request.GET.get('application_number', '').strip()
        application = AdmissionApplication.objects.filter(
            application_number__iexact=application_number,
        ).select_related('program', 'preferred_department', 'user').first()
        if not application:
            messages.error(request, 'No application found for this GCMS application number.')
    elif request.user.is_authenticated and request.user.user_type == 'student':
        application = AdmissionApplication.objects.filter(user=request.user).select_related(
            'program', 'preferred_department'
        ).first()

    return render(request, 'admissions/status.html', {
        'application': application,
        'page_title': 'Admission Status',
    })
