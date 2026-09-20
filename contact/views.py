from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage
from core.models import SiteSettings


def contact(request):
    site = SiteSettings.get_settings()
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()
        if name and email and subject and message_text:
            ip = request.META.get('REMOTE_ADDR')
            ContactMessage.objects.create(
                name=name, email=email, phone=phone,
                subject=subject, message=message_text, ip_address=ip
            )
            messages.success(request, 'Your message has been sent successfully. We will get back to you soon.')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill in all required fields.')
    return render(request, 'contact/contact.html', {
        'site': site,
        'page_title': 'Contact Us',
    })
