"""
URL configuration for fitness_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns # Import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import ArticleSitemap, CategorySitemap, StaticSitemap
from django.views.decorators.cache import cache_page

sitemaps = {
    'articles': ArticleSitemap,
    'categories': CategorySitemap,
    'static': StaticSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('sitemap.xml', 
        cache_page(86400)(sitemap),  # Cache pentru 24 ore
        {'sitemaps': sitemaps,
         'template_name': 'sitemap.xml',
         'content_type': 'application/xml'},
        name='django.contrib.sitemaps.views.sitemap'
    ),
    path('robots.txt', 
        TemplateView.as_view(
            template_name="robots.txt", 
            content_type="text/plain"
        )
    ),
    path('ads.txt', 
        TemplateView.as_view(
            template_name="ads.txt", 
            content_type="text/plain"
        ),
        name='ads_txt'
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Add this line to serve static files during development
    urlpatterns += staticfiles_urlpatterns()
