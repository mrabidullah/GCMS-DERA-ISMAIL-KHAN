from django.shortcuts import render, get_object_or_404, redirect
from .models import DownloadFile, DownloadCategory


def downloads_list(request):
    categories = DownloadCategory.objects.all()
    cat_slug = request.GET.get('category', '')
    files = DownloadFile.objects.filter(is_active=True)
    if cat_slug:
        files = files.filter(category__slug=cat_slug)
    return render(request, 'downloads/list.html', {
        'files': files,
        'categories': categories,
        'cat_slug': cat_slug,
        'page_title': 'Downloads',
    })


def download_file(request, pk):
    dl = get_object_or_404(DownloadFile, pk=pk, is_active=True)
    dl.download_count += 1
    dl.save(update_fields=['download_count'])
    return redirect(dl.file.url)
