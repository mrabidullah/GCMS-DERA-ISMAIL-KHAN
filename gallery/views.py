from django.shortcuts import render, get_object_or_404
from .models import GalleryAlbum, GalleryItem


def gallery_list(request):
    albums = GalleryAlbum.objects.filter(is_active=True)
    return render(request, 'gallery/list.html', {
        'albums': albums,
        'page_title': 'Gallery',
    })


def gallery_detail(request, slug):
    album = get_object_or_404(GalleryAlbum, slug=slug, is_active=True)
    items = album.items.all()
    return render(request, 'gallery/detail.html', {
        'album': album,
        'items': items,
        'page_title': album.title,
    })
