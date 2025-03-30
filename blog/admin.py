from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Article, AdSenseLocation, NewsletterSubscriber

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    
    class Meta:
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categorii'

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'display_image')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informații de bază', {
            'fields': ('title', 'slug', 'category', 'featured_image')
        }),
        ('Conținut', {
            'fields': ('content', 'read_time')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Informații temporale', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def display_image(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.featured_image.url)
        return "Fără imagine"
    display_image.short_description = 'Imagine'

    class Meta:
        verbose_name = 'Articol'
        verbose_name_plural = 'Articole'

class AdSenseLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_editable = ('is_active',)
    
    class Meta:
        verbose_name = 'Locație AdSense'
        verbose_name_plural = 'Locații AdSense'

class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)
    
    class Meta:
        verbose_name = 'Abonat Newsletter'
        verbose_name_plural = 'Abonați Newsletter'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(AdSenseLocation, AdSenseLocationAdmin)
admin.site.register(NewsletterSubscriber, NewsletterSubscriberAdmin)

# Personalizare titluri admin
admin.site.site_header = 'Administrare Blog Fitness'
admin.site.site_title = 'Panou de administrare'
admin.site.index_title = 'Bine ați venit la panoul de administrare'
