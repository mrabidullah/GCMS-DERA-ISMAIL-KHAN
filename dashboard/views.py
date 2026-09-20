from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse


def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.user_type == 'admin')


def admin_required(view_func):
    decorated = user_passes_test(is_admin, login_url='/accounts/login/')(view_func)
    return login_required(decorated)


@admin_required
def dashboard_home(request):
    from news.models import NewsArticle
    from faculty.models import FacultyMember
    from accounts.models import CustomUser, RegistrationRequest
    from contact.models import ContactMessage
    from departments.models import Department
    from events.models import Event
    from announcements.models import Announcement
    from admissions.models import AdmissionApplication
    context = {
        'total_news': NewsArticle.objects.count(),
        'published_news': NewsArticle.objects.filter(status='published').count(),
        'total_faculty': FacultyMember.objects.filter(is_active=True).count(),
        'total_departments': Department.objects.filter(is_active=True).count(),
        'total_students': CustomUser.objects.filter(user_type='student').count(),
        'total_teachers': CustomUser.objects.filter(user_type='teacher').count(),
        'pending_registrations': RegistrationRequest.objects.filter(status='pending').count(),
        'pending_admissions': AdmissionApplication.objects.filter(status__in=['pending', 'waiting']).count(),
        'unread_messages': ContactMessage.objects.filter(status='new').count(),
        'upcoming_events': Event.objects.filter(is_active=True, event_date__gte=timezone.now().date()).count(),
        'active_announcements': Announcement.objects.filter(is_active=True).count(),
        'recent_messages': ContactMessage.objects.filter(status='new')[:5],
        'pending_regs': RegistrationRequest.objects.filter(status='pending').select_related('user')[:5],
        'pending_admission_apps': AdmissionApplication.objects.filter(status__in=['pending', 'waiting']).select_related('program')[:5],
        'page_title': 'Admin Dashboard',
    }
    return render(request, 'dashboard/home.html', context)


@admin_required
def manage_hero(request):
    from homepage.models import HeroSlide
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            slide = HeroSlide(
                title=request.POST.get('title', ''),
                subtitle=request.POST.get('subtitle', ''),
                description=request.POST.get('description', ''),
                button_text=request.POST.get('button_text', 'Learn More'),
                button_link=request.POST.get('button_link', '#'),
                button2_text=request.POST.get('button2_text', ''),
                button2_link=request.POST.get('button2_link', ''),
                order=int(request.POST.get('order', 0)),
                is_active=request.POST.get('is_active') == 'on',
            )
            if 'background_image' in request.FILES:
                slide.background_image = request.FILES['background_image']
            slide.save()
            messages.success(request, 'Slide created.')
        elif action == 'delete':
            slide_id = request.POST.get('slide_id')
            HeroSlide.objects.filter(pk=slide_id).delete()
            messages.success(request, 'Slide deleted.')
        elif action == 'toggle':
            slide_id = request.POST.get('slide_id')
            slide = HeroSlide.objects.filter(pk=slide_id).first()
            if slide:
                slide.is_active = not slide.is_active
                slide.save()
        return redirect('manage_hero')
    slides = HeroSlide.objects.all()
    return render(request, 'dashboard/hero.html', {'slides': slides, 'page_title': 'Manage Hero Section'})


@admin_required
def manage_news(request):
    from news.models import NewsArticle, NewsCategory
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            category_id = request.POST.get('category')
            category = None
            if category_id:
                from news.models import NewsCategory
                category = NewsCategory.objects.filter(pk=category_id).first()
            article = NewsArticle(
                title=request.POST.get('title', ''),
                excerpt=request.POST.get('excerpt', ''),
                content=request.POST.get('content', ''),
                category=category,
                status=request.POST.get('status', 'draft'),
                is_featured=request.POST.get('is_featured') == 'on',
            )
            if 'image' in request.FILES:
                article.image = request.FILES['image']
            article.save()
            messages.success(request, 'News article saved.')
        elif action == 'delete':
            NewsArticle.objects.filter(pk=request.POST.get('article_id')).delete()
            messages.success(request, 'Article deleted.')
        elif action == 'toggle_status':
            article = NewsArticle.objects.filter(pk=request.POST.get('article_id')).first()
            if article:
                article.status = 'published' if article.status == 'draft' else 'draft'
                article.save()
        return redirect('manage_news')
    articles = NewsArticle.objects.all()[:50]
    categories = NewsCategory.objects.all()
    return render(request, 'dashboard/news.html', {
        'articles': articles,
        'categories': categories,
        'page_title': 'Manage News',
    })


@admin_required
def manage_announcements(request):
    from announcements.models import Announcement
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            Announcement.objects.create(
                title=request.POST.get('title', ''),
                content=request.POST.get('content', ''),
                priority=request.POST.get('priority', 'normal'),
                is_pinned=request.POST.get('is_pinned') == 'on',
                expiry_date=request.POST.get('expiry_date') or None,
                is_active=True,
            )
            messages.success(request, 'Announcement created.')
        elif action == 'delete':
            Announcement.objects.filter(pk=request.POST.get('id')).delete()
            messages.success(request, 'Announcement deleted.')
        return redirect('manage_announcements')
    announcements = Announcement.objects.all()
    return render(request, 'dashboard/announcements.html', {
        'announcements': announcements,
        'page_title': 'Manage Announcements',
    })


@admin_required
def manage_faculty(request):
    from faculty.models import FacultyMember
    from departments.models import Department
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete':
            FacultyMember.objects.filter(pk=request.POST.get('id')).delete()
            messages.success(request, 'Faculty member deleted.')
        elif action == 'toggle':
            member = FacultyMember.objects.filter(pk=request.POST.get('id')).first()
            if member:
                member.is_active = not member.is_active
                member.save()
        elif action == 'create':
            dept_id = request.POST.get('department')
            dept = Department.objects.filter(pk=dept_id).first() if dept_id else None
            member = FacultyMember(
                name=request.POST.get('name', ''),
                designation=request.POST.get('designation', ''),
                qualification=request.POST.get('qualification', ''),
                department=dept,
                biography=request.POST.get('biography', ''),
                email=request.POST.get('email', ''),
                office_hours=request.POST.get('office_hours', ''),
                specialization=request.POST.get('specialization', ''),
                experience_years=int(request.POST.get('experience_years', 0) or 0),
                is_featured=request.POST.get('is_featured') == 'on',
            )
            if 'photo' in request.FILES:
                member.photo = request.FILES['photo']
            member.save()
            messages.success(request, 'Faculty member added.')
        return redirect('manage_faculty')
    faculty = FacultyMember.objects.all()
    departments = Department.objects.filter(is_active=True)
    return render(request, 'dashboard/faculty.html', {
        'faculty': faculty,
        'departments': departments,
        'page_title': 'Manage Faculty',
    })


@admin_required
def manage_registrations(request):
    from accounts.models import RegistrationRequest
    if request.method == 'POST':
        req_id = request.POST.get('req_id')
        action = request.POST.get('action')
        reg = get_object_or_404(RegistrationRequest, pk=req_id)
        if action == 'approve':
            reg.status = 'approved'
            reg.user.is_approved = True
            reg.user.is_active = True
            reg.reviewed_at = timezone.now()
            reg.user.save()
            reg.save()
            messages.success(request, f'{reg.user.get_full_name() or reg.user.username} approved.')
        elif action == 'reject':
            reg.status = 'rejected'
            reg.reviewed_at = timezone.now()
            reg.save()
            messages.success(request, 'Registration rejected.')
        return redirect('manage_registrations')
    regs = RegistrationRequest.objects.select_related('user').all()
    return render(request, 'dashboard/registrations.html', {
        'regs': regs,
        'page_title': 'Registration Requests',
    })


@admin_required
def manage_admissions(request):
    from admissions.models import AdmissionApplication
    if request.method == 'POST':
        application = get_object_or_404(AdmissionApplication, pk=request.POST.get('application_id'))
        action = request.POST.get('action')
        if action in ['pending', 'waiting', 'confirmed', 'rejected']:
            application.status = action
            application.admin_notes = request.POST.get('admin_notes', application.admin_notes)
            application.reviewed_at = timezone.now()
            application.save()
            messages.success(request, f'{application.application_number} marked as {application.get_status_display()}.')
        return redirect('manage_admissions')

    status = request.GET.get('status', '')
    applications = AdmissionApplication.objects.select_related('program', 'preferred_department', 'user')
    if status:
        applications = applications.filter(status=status)
    return render(request, 'dashboard/admissions.html', {
        'applications': applications,
        'status': status,
        'status_choices': AdmissionApplication.STATUS_CHOICES,
        'page_title': 'Admission Applications',
    })


@admin_required
def manage_site_settings(request):
    from core.models import SiteSettings
    site = SiteSettings.get_settings()
    if request.method == 'POST':
        site.site_name = request.POST.get('site_name', site.site_name)
        site.site_tagline = request.POST.get('site_tagline', site.site_tagline)
        site.contact_email = request.POST.get('contact_email', site.contact_email)
        site.contact_phone = request.POST.get('contact_phone', site.contact_phone)
        site.contact_phone2 = request.POST.get('contact_phone2', site.contact_phone2)
        site.contact_address = request.POST.get('contact_address', site.contact_address)
        site.office_hours = request.POST.get('office_hours', site.office_hours)
        site.google_map_embed = request.POST.get('google_map_embed', site.google_map_embed)
        site.facebook_url = request.POST.get('facebook_url', site.facebook_url)
        site.twitter_url = request.POST.get('twitter_url', site.twitter_url)
        site.youtube_url = request.POST.get('youtube_url', site.youtube_url)
        site.instagram_url = request.POST.get('instagram_url', site.instagram_url)
        site.footer_text = request.POST.get('footer_text', site.footer_text)
        site.is_admission_open = request.POST.get('is_admission_open') == 'on'
        site.admission_banner_text = request.POST.get('admission_banner_text', site.admission_banner_text)
        if 'site_logo' in request.FILES:
            site.site_logo = request.FILES['site_logo']
        site.save()
        messages.success(request, 'Site settings updated.')
        return redirect('manage_site_settings')
    return render(request, 'dashboard/site_settings.html', {
        'site': site,
        'page_title': 'Site Settings',
    })


@admin_required
def manage_departments(request):
    from departments.models import Department
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            dept = Department(
                name=request.POST.get('name', ''),
                short_name=request.POST.get('short_name', ''),
                description=request.POST.get('description', ''),
                hod_name=request.POST.get('hod_name', ''),
                order=int(request.POST.get('order', 0) or 0),
            )
            if 'image' in request.FILES:
                dept.image = request.FILES['image']
            dept.save()
            messages.success(request, 'Department created.')
        elif action == 'delete':
            Department.objects.filter(pk=request.POST.get('id')).delete()
            messages.success(request, 'Department deleted.')
        return redirect('manage_departments')
    departments = Department.objects.all()
    return render(request, 'dashboard/departments.html', {
        'departments': departments,
        'page_title': 'Manage Departments',
    })


@admin_required
def manage_gallery(request):
    from gallery.models import GalleryAlbum, GalleryItem
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create_album':
            album = GalleryAlbum(
                title=request.POST.get('title', ''),
                description=request.POST.get('description', ''),
            )
            if 'cover_image' in request.FILES:
                album.cover_image = request.FILES['cover_image']
            album.save()
            messages.success(request, 'Album created.')
        elif action == 'add_image':
            album = get_object_or_404(GalleryAlbum, pk=request.POST.get('album_id'))
            for f in request.FILES.getlist('images'):
                GalleryItem.objects.create(
                    album=album, item_type='image', image=f,
                    title=request.POST.get('title', f.name)
                )
            messages.success(request, 'Images uploaded.')
        elif action == 'delete_album':
            GalleryAlbum.objects.filter(pk=request.POST.get('album_id')).delete()
            messages.success(request, 'Album deleted.')
        return redirect('manage_gallery')
    albums = GalleryAlbum.objects.all()
    return render(request, 'dashboard/gallery.html', {
        'albums': albums,
        'page_title': 'Manage Gallery',
    })


@admin_required
def manage_events(request):
    from events.models import Event
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            ev = Event(
                title=request.POST.get('title', ''),
                description=request.POST.get('description', ''),
                event_date=request.POST.get('event_date'),
                location=request.POST.get('location', ''),
                organizer=request.POST.get('organizer', ''),
                is_featured=request.POST.get('is_featured') == 'on',
            )
            if 'image' in request.FILES:
                ev.image = request.FILES['image']
            ev.save()
            messages.success(request, 'Event created.')
        elif action == 'delete':
            Event.objects.filter(pk=request.POST.get('id')).delete()
            messages.success(request, 'Event deleted.')
        return redirect('manage_events')
    events = Event.objects.all()
    return render(request, 'dashboard/events.html', {
        'events': events,
        'page_title': 'Manage Events',
    })


@admin_required
def manage_downloads(request):
    from downloads.models import DownloadFile, DownloadCategory
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'upload':
            cat_id = request.POST.get('category')
            cat = DownloadCategory.objects.filter(pk=cat_id).first() if cat_id else None
            if 'file' in request.FILES:
                f = request.FILES['file']
                DownloadFile.objects.create(
                    title=request.POST.get('title', f.name),
                    description=request.POST.get('description', ''),
                    file=f,
                    category=cat,
                )
                messages.success(request, 'File uploaded.')
        elif action == 'delete':
            DownloadFile.objects.filter(pk=request.POST.get('id')).delete()
            messages.success(request, 'File deleted.')
        return redirect('manage_downloads')
    files = DownloadFile.objects.all()
    categories = DownloadCategory.objects.all()
    return render(request, 'dashboard/downloads.html', {
        'files': files,
        'categories': categories,
        'page_title': 'Manage Downloads',
    })


@admin_required
def manage_messages(request):
    from contact.models import ContactMessage
    if request.method == 'POST':
        msg_id = request.POST.get('id')
        action = request.POST.get('action')
        msg = ContactMessage.objects.filter(pk=msg_id).first()
        if msg:
            if action == 'mark_read':
                msg.status = 'read'
                msg.save()
            elif action == 'delete':
                msg.delete()
        return redirect('manage_messages')
    msgs = ContactMessage.objects.all()
    return render(request, 'dashboard/messages.html', {
        'msgs': msgs,
        'page_title': 'Contact Messages',
    })


@admin_required
def manage_principal_message(request):
    from homepage.models import PrincipalMessage
    msg = PrincipalMessage.objects.first()
    if not msg:
        msg = PrincipalMessage()
    if request.method == 'POST':
        msg.name = request.POST.get('name', msg.name)
        msg.designation = request.POST.get('designation', msg.designation)
        msg.message = request.POST.get('message', msg.message)
        msg.qualification = request.POST.get('qualification', msg.qualification)
        msg.is_active = request.POST.get('is_active') == 'on'
        if 'photo' in request.FILES:
            msg.photo = request.FILES['photo']
        msg.save()
        messages.success(request, "Principal's message updated.")
        return redirect('manage_principal_message')
    return render(request, 'dashboard/principal_message.html', {
        'msg': msg,
        'page_title': "Principal's Message",
    })


@admin_required
def manage_video(request):
    from homepage.models import FeaturedVideo
    videos = FeaturedVideo.objects.all()
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            v = FeaturedVideo(
                title=request.POST.get('title', ''),
                video_type=request.POST.get('video_type', 'youtube'),
                video_url=request.POST.get('video_url', ''),
                description=request.POST.get('description', ''),
                is_featured=request.POST.get('is_featured') == 'on',
            )
            if 'thumbnail' in request.FILES:
                v.thumbnail = request.FILES['thumbnail']
            if 'video_file' in request.FILES:
                v.video_file = request.FILES['video_file']
            v.save()
            messages.success(request, 'Video added.')
        elif action == 'delete':
            FeaturedVideo.objects.filter(pk=request.POST.get('id')).delete()
            messages.success(request, 'Video deleted.')
        return redirect('manage_video')
    return render(request, 'dashboard/video.html', {
        'videos': videos,
        'page_title': 'Manage Videos',
    })
