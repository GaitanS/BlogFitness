from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Article, Category

class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Article.objects.all().order_by('-created_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f'/articol/{obj.slug}/'

class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return f'/categorie/{obj.slug}/'

class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['home', 'bmi_calculator']

    def location(self, item):
        return reverse(item)
