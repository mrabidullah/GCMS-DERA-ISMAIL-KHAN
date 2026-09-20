from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import CustomUser, StudentProfile, TeacherProfile, RegistrationRequest, LoginLog
from departments.models import Department


def register(request):
    departments = Department.objects.filter(is_active=True)
    if request.method == 'POST':
        user_type = request.POST.get('user_type', 'student')
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'accounts/register.html', {'departments': departments})

        user = CustomUser(
            username=username,
            email=email,
            user_type=user_type,
            phone=phone,
            is_active=False,
            is_approved=False,
        )
        user.set_password(password)

        if user_type == 'student':
            user.first_name = request.POST.get('student_name', '').split()[0] if request.POST.get('student_name') else ''
            user.last_name = ' '.join(request.POST.get('student_name', '').split()[1:]) if request.POST.get('student_name') else ''
        else:
            user.first_name = request.POST.get('teacher_name', '').split()[0] if request.POST.get('teacher_name') else ''
            user.last_name = ' '.join(request.POST.get('teacher_name', '').split()[1:]) if request.POST.get('teacher_name') else ''

        user.save()

        if user_type == 'student':
            dept_id = request.POST.get('department')
            dept = Department.objects.filter(pk=dept_id).first() if dept_id else None
            StudentProfile.objects.create(
                user=user,
                roll_number=request.POST.get('roll_number', ''),
                registration_number=request.POST.get('registration_number', ''),
                father_name=request.POST.get('father_name', ''),
                cnic=request.POST.get('cnic', ''),
                department=dept,
                semester=request.POST.get('semester', ''),
                session=request.POST.get('session', ''),
            )
        else:
            dept_id = request.POST.get('teacher_department')
            dept = Department.objects.filter(pk=dept_id).first() if dept_id else None
            TeacherProfile.objects.create(
                user=user,
                employee_id=request.POST.get('employee_id', ''),
                qualification=request.POST.get('qualification', ''),
                designation=request.POST.get('designation', ''),
                department=dept,
                experience=request.POST.get('experience', ''),
                specialization=request.POST.get('specialization', ''),
            )

        RegistrationRequest.objects.create(user=user)
        messages.success(request, 'Your registration request has been submitted successfully. Please wait for the administrator\'s approval.')
        return redirect('registration_submitted')

    return render(request, 'accounts/register.html', {'departments': departments})


def registration_submitted(request):
    return render(request, 'accounts/registration_submitted.html', {'page_title': 'Registration Submitted'})


def user_login(request):
    if request.user.is_authenticated:
        return redirect_after_login(request.user)
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user:
            if not user.is_approved and not user.is_staff:
                messages.error(request, 'Your account is pending approval. Please wait for administrator approval.')
                return render(request, 'accounts/login.html')
            login(request, user)
            # Log the login
            LoginLog.objects.create(
                user=user,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:200]
            )
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect_after_login(user)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html', {'page_title': 'Login'})


def redirect_after_login(user):
    if user.is_staff or user.user_type == 'admin':
        return redirect('dashboard_home')
    elif user.user_type == 'teacher':
        return redirect('teacher_portal')
    else:
        return redirect('student_portal')


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def student_portal(request):
    if request.user.user_type != 'student' and not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    profile = getattr(request.user, 'student_profile', None)
    from news.models import NewsArticle
    from announcements.models import Announcement
    from events.models import Event
    from downloads.models import DownloadFile
    from admissions.models import AdmissionApplication
    news = NewsArticle.objects.filter(status='published')[:5]
    announcements = Announcement.objects.filter(is_active=True)[:5]
    events = Event.objects.filter(is_active=True, event_date__gte=timezone.now().date())[:5]
    downloads = DownloadFile.objects.filter(is_active=True)[:10]
    admission_applications = AdmissionApplication.objects.filter(user=request.user).select_related('program')
    return render(request, 'accounts/student_portal.html', {
        'profile': profile,
        'news': news,
        'announcements': announcements,
        'events': events,
        'downloads': downloads,
        'admission_applications': admission_applications,
        'page_title': 'Student Portal',
    })


@login_required
def teacher_portal(request):
    if request.user.user_type != 'teacher' and not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    profile = getattr(request.user, 'teacher_profile', None)
    return render(request, 'accounts/teacher_portal.html', {
        'profile': profile,
        'page_title': 'Teacher Portal',
    })


@login_required
def edit_profile(request):
    user = request.user
    student_profile = getattr(user, 'student_profile', None)
    teacher_profile = getattr(user, 'teacher_profile', None)
    if request.method == 'POST':
        user.phone = request.POST.get('phone', user.phone)
        user.address = request.POST.get('address', user.address)
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        user.save()
        if teacher_profile:
            teacher_profile.biography = request.POST.get('biography', teacher_profile.biography)
            teacher_profile.office_hours = request.POST.get('office_hours', teacher_profile.office_hours)
            teacher_profile.qualification = request.POST.get('qualification', teacher_profile.qualification)
            teacher_profile.specialization = request.POST.get('specialization', teacher_profile.specialization)
            teacher_profile.profile_changes_pending = True
            teacher_profile.save()
        messages.success(request, 'Profile updated successfully.')
        if user.user_type == 'teacher':
            return redirect('teacher_portal')
        return redirect('student_portal')
    return render(request, 'accounts/edit_profile.html', {
        'student_profile': student_profile,
        'teacher_profile': teacher_profile,
        'page_title': 'Edit Profile',
    })


@login_required
def change_password(request):
    if request.method == 'POST':
        old = request.POST.get('old_password', '')
        new = request.POST.get('new_password', '')
        confirm = request.POST.get('confirm_password', '')
        if not request.user.check_password(old):
            messages.error(request, 'Current password is incorrect.')
        elif new != confirm:
            messages.error(request, 'New passwords do not match.')
        elif len(new) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
        else:
            request.user.set_password(new)
            request.user.save()
            messages.success(request, 'Password changed successfully. Please log in again.')
            return redirect('login')
    return render(request, 'accounts/change_password.html', {'page_title': 'Change Password'})
