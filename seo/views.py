from django.http import HttpResponse

def robots_txt(request):
    content = """User-agent: *
Allow: /
Disallow: /django-admin/
Disallow: /dashboard/

Sitemap: /sitemap.xml
"""
    return HttpResponse(content, content_type='text/plain')
