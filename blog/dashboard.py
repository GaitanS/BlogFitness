from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from django.utils.html import format_html
from django.db.models.functions import TruncMonth

from .models import Article, Category, NewsletterSubscriber

def get_admin_url(obj):
    """
    Return the admin URL for an object
    """
    # Temporarily return a hash to avoid reverse errors
    return "#"

def get_article_stats():
    """
    Return statistics about articles
    """
    total_articles = Article.objects.count()
    articles_by_category = list(
        Category.objects.annotate(article_count=Count('articles')).values('name', 'article_count', 'id')
    )
    
    # Format data for pie chart
    for item in articles_by_category:
        item['url'] = '#'  # Disable URL for now to avoid reverse error
    
    # Get recent articles
    recent_articles = Article.objects.order_by('-created_at')[:5]
    recent_articles_html = []
    
    for article in recent_articles:
        admin_url = get_admin_url(article)
        recent_articles_html.append(
            format_html(
                '<li><a href="{}">{}</a> <span class="text-muted">({} min)</span></li>',
                admin_url, article.title, article.read_time
            )
        )
    
    # Get articles by month
    last_6_months = timezone.now() - timedelta(days=180)
    articles_by_month = (
        Article.objects
        .filter(created_at__gte=last_6_months)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    
    return {
        'total_articles': total_articles,
        'articles_by_category': articles_by_category,
        'recent_articles_html': recent_articles_html,
        'articles_by_month': list(articles_by_month),
    }

def get_subscriber_stats():
    """
    Return statistics about newsletter subscribers
    """
    total_subscribers = NewsletterSubscriber.objects.count()
    
    # Get subscribers by month
    last_6_months = timezone.now() - timedelta(days=180)
    subscribers_by_month = (
        NewsletterSubscriber.objects
        .filter(subscribed_at__gte=last_6_months)
        .annotate(month=TruncMonth('subscribed_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    
    # Get recent subscribers
    recent_subscribers = NewsletterSubscriber.objects.order_by('-subscribed_at')[:5]
    recent_subscribers_html = []
    
    for subscriber in recent_subscribers:
        admin_url = get_admin_url(subscriber)
        recent_subscribers_html.append(
            format_html(
                '<li><a href="{}">{}</a> <span class="text-muted">({})</span></li>',
                admin_url, subscriber.email, subscriber.subscribed_at.strftime('%d.%m.%Y')
            )
        )
    
    return {
        'total_subscribers': total_subscribers,
        'subscribers_by_month': list(subscribers_by_month),
        'recent_subscribers_html': recent_subscribers_html,
    }
