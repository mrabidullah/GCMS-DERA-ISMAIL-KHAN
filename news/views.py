from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import NewsArticle, NewsCategory


def news_list(request):
    articles = NewsArticle.objects.filter(status='published')
    category_slug = request.GET.get('category', '')
    categories = NewsCategory.objects.all()
    if category_slug:
        articles = articles.filter(category__slug=category_slug)
    paginator = Paginator(articles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'category_slug': category_slug,
        'page_title': 'News',
    })


def news_detail(request, slug):
    article = get_object_or_404(NewsArticle, slug=slug, status='published')
    related = NewsArticle.objects.filter(
        status='published', category=article.category
    ).exclude(pk=article.pk)[:3]
    return render(request, 'news/detail.html', {
        'article': article,
        'related': related,
        'page_title': article.title,
    })
