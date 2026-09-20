from .models import SiteSettings
from departments.models import Department
from news.models import NewsArticle
from announcements.models import Announcement


def site_settings(request):
    settings = SiteSettings.get_settings()
    return {'site_settings': settings}


def navigation_data(request):
    departments = Department.objects.filter(is_active=True).order_by('name')
    return {'nav_departments': departments}
