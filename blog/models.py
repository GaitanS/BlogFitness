from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nume')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name='Iconiță FontAwesome')

    class Meta:
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categorii'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Titlu')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    content = RichTextField(verbose_name='Conținut')
    featured_image = models.ImageField(upload_to='articles/', verbose_name='Imagine principală')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles', verbose_name='Categorie')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data creării')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data actualizării')
    read_time = models.IntegerField(default=5, verbose_name='Timp de citire (minute)')
    
    # SEO fields
    meta_title = models.CharField(max_length=200, blank=True, verbose_name='Titlu Meta')
    meta_description = models.TextField(blank=True, verbose_name='Descriere Meta')
    meta_keywords = models.CharField(max_length=200, blank=True, verbose_name='Cuvinte cheie Meta')

    class Meta:
        verbose_name = 'Articol'
        verbose_name_plural = 'Articole'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title
        super().save(*args, **kwargs)


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email


class AdSenseLocation(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nume locație')
    ad_code = models.TextField(verbose_name='Cod AdSense')
    is_active = models.BooleanField(default=True, verbose_name='Este activ')

    class Meta:
        verbose_name = 'Locație AdSense'
        verbose_name_plural = 'Locații AdSense'
        ordering = ['name']

    def __str__(self):
        return self.name
