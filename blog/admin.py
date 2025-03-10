from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, Article, NewsletterSubscriber, AdSenseLocation
from .dashboard import get_article_stats, get_subscriber_stats

# Custom admin site
admin.site.site_header = "Fitness Blog Admin"
admin.site.site_title = "Fitness Blog Admin Portal"
admin.site.index_title = "Bine ai venit în panoul de administrare"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'article_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    
    def article_count(self, obj):
        count = obj.articles.count()
        url = reverse('admin:blog_article_changelist') + f'?category__id__exact={obj.id}'
        return format_html('<a href="{}">{} articole</a>', url, count)
    
    article_count.short_description = 'Articole'

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'read_time', 'is_featured', 'created_at', 'preview_image')
    list_filter = ('category', 'is_featured', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'
    readonly_fields = ('preview_image_large',)
    
    def preview_image(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.featured_image.url)
        return "-"
    
    preview_image.short_description = 'Imagine'
    
    def preview_image_large(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="300" style="max-height: 300px; object-fit: contain;" />', obj.featured_image.url)
        return "-"
    
    preview_image_large.short_description = 'Previzualizare imagine'
    
    fieldsets = (
        ('Informații de bază', {
            'fields': ('title', 'slug', 'category', 'read_time', 'is_featured')
        }),
        ('Conținut', {
            'fields': ('content',)
        }),
        ('Imagine', {
            'fields': ('featured_image', 'preview_image_large')
        }),
    )

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    date_hierarchy = 'subscribed_at'
    
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(AdSenseLocation)
class AdSenseLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'description_short')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    
    def description_short(self, obj):
        if obj.description and len(obj.description) > 50:
            return obj.description[:50] + '...'
        return obj.description
    
    description_short.short_description = 'Descriere'
