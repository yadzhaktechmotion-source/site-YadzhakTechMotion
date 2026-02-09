from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import FileResponse, HttpResponse
from django.views.i18n import set_language
from blog import views as blog_views
from blog.models import SiteSettings
import os

def favicon_view(request):
    site = SiteSettings.objects.first()
    if site and site.logo and os.path.exists(site.logo.path):
        return FileResponse(open(site.logo.path, 'rb'), content_type='image/x-icon')

    fallback = os.path.join(settings.STATIC_ROOT or '', 'favicon.ico')
    if os.path.exists(fallback):
        return FileResponse(open(fallback, 'rb'), content_type='image/x-icon')

    return HttpResponse(status=404)


def robots_view(request):
    content = (
        "User-agent: *\n"
        "Disallow:\n"
        f"Sitemap: https://{getattr(settings, 'SITE_DOMAIN', 'yourdomain.com')}/sitemap.xml\n"
    )
    return HttpResponse(content, content_type="text/plain")


urlpatterns = [
    # Admin area
    path('admin-romashka/', admin.site.urls),

    # Blog routes
    path('', include('blog.urls')),

    # Auth (email-code)
    path('', include('accounts.urls')),

    # Language switcher
    path('setlang/', set_language, name='set_language'),

    # Favicon & robots.txt
    path('favicon.ico', favicon_view, name='favicon'),
    path('robots.txt', robots_view, name='robots'),
]

handler403 = "blog.views.error_403"
handler404 = "blog.views.error_404"
handler500 = "blog.views.error_500"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
