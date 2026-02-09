from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Category, Article, SiteSettings

def error_403(request, exception):
    return render(request, "error/403.html", status=403)

def error_404(request, exception):
    return render(request, "error/404.html", status=404)

def error_500(request):
    return render(request, "error/500.html", status=500)

def home(request):
    return render(request, 'blog/home.html')

def about(request):
    settings_obj = SiteSettings.objects.first()
    return render(request, 'blog/about.html', {'settings_obj': settings_obj})

def help_page(request):
    return render(request, 'blog/help.html')

def devops_map(request):
    categories = Category.objects.all()
    return render(request, 'blog/map.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    qs = category.articles.filter(language=request.LANGUAGE_CODE[:2])

    if not request.user.is_authenticated:
        qs = qs.filter(published=True, public=True, is_pro=False)
    else:
        if not getattr(request.user, "is_pro", False):
            qs = qs.exclude(is_pro=True)

    return render(request, 'blog/article.html', {'category': category, 'articles': qs})


def support(request):
    settings_obj = SiteSettings.objects.first()
    return render(request, 'blog/support.html', {'settings_obj': settings_obj})

def article_pdf_view(request, slug):
    article = get_object_or_404(Article, slug=slug)
    settings_obj = SiteSettings.objects.first()

    if article.is_pro:
        if not request.user.is_authenticated or not getattr(request.user, "is_pro", False):
            return render(request, 'blog/article_pdf.html', {
                'article': None,
                'settings_obj': settings_obj,
                'pro_required': True,
            })

    if not request.user.is_authenticated and (not article.public or not article.published):
        return render(request, 'blog/article_pdf.html', {'article': None, 'settings_obj': settings_obj})

    return render(request, 'blog/article_pdf.html', {'article': article, 'settings_obj': settings_obj})

def vote_article(request, article_id, action):
    article = get_object_or_404(Article, id=article_id)
    now = timezone.now()
    last_vote = request.session.get(f"vote_{article_id}")
    last_time = request.session.get(f"vote_time_{article_id}")
    if last_vote == action and last_time:
        del request.session[f"vote_{article_id}"]
        del request.session[f"vote_time_{article_id}"]
        if action == "like" and article.likes > 0:
            article.likes -= 1
        elif action == "dislike" and article.dislikes > 0:
            article.dislikes -= 1
        article.save()
        return JsonResponse({'likes': article.likes, 'dislikes': article.dislikes, 'status': 'cancelled'})
    if last_time:
        last_time = timezone.datetime.fromisoformat(last_time)
        if now - last_time < timedelta(hours=3):
            return JsonResponse({'error': 'You can vote again after 3 hours.'}, status=403)
    if action == "like":
        article.likes += 1
    elif action == "dislike":
        article.dislikes += 1
    article.save()
    request.session[f"vote_{article_id}"] = action
    request.session[f"vote_time_{article_id}"] = now.isoformat()
    return JsonResponse({'likes': article.likes, 'dislikes': article.dislikes, 'status': 'voted'})
