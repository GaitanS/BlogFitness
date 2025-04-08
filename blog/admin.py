from django.contrib import admin
from .models import Category, Article, AdSenseLocation, NewsletterSubscriber, SiteSettings

# Înregistrează modelele cu admin-ul standard Django
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(AdSenseLocation)
admin.site.register(NewsletterSubscriber)
admin.site.register(SiteSettings)
