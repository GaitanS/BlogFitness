from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse
from django.db.models import Count
# from django.views.decorators.csrf import csrf_exempt # Removed csrf_exempt
from django.core.paginator import Paginator
from .models import Category, Article, NewsletterSubscriber, AdSenseLocation
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.decorators.cache import cache_page
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

def get_adsense_locations():
    return {
        ad.name: ad.ad_code 
        for ad in AdSenseLocation.objects.filter(is_active=True)
    }

@cache_page(60 * 15)  # Cache pentru 15 minute
def home(request):
    # Get the latest article
    latest_article = Article.objects.order_by('-created_at').select_related('category').first()
    
    # Get categories with at least one article
    categories = Category.objects.annotate(
        articles_count=Count('articles')
    ).filter(articles_count__gt=0)
    
    # Get all recent articles, ordered by creation date (descending)
    recent_articles = Article.objects.select_related('category').order_by('-created_at')[:9]  # Limit to 9 articles for the recommended section
    
    # Initialize the ordered dictionary for category articles
    category_articles = {}
    
    # Add articles for all categories - asigură-te că sunt ordonate după data creării (descrescător)
    for category in categories:
        # Obține articolele pentru această categorie, ordonate după data creării (de la cel mai nou la cel mai vechi)
        category_articles[category] = Article.objects.filter(
            category=category
        ).order_by('-created_at')[:3]  # Primele 3 articole cele mai recente
    
    context = {
        'latest_article': latest_article,
        'categories': categories,
        'category_articles': category_articles,
        'recent_articles': recent_articles,
        'adsense_locations': get_adsense_locations(),
    }
    
    return render(request, 'blog/home.html', context)

def article_detail(request, slug):
    try:
        article = get_object_or_404(Article, slug=slug)
        related_articles = Article.objects.filter(
            category=article.category
        ).exclude(id=article.id).order_by('-created_at')[:3]
        
        context = {
            'article': article,
            'related_articles': related_articles,
            'adsense_locations': get_adsense_locations(),
        }
        
        return render(request, 'blog/article_detail.html', context)
    except Exception as e:
        logger.error(f"Error in article_detail view: {str(e)}")
        raise

def category_articles(request, slug):
    # Get category and ensure it exists
    category = get_object_or_404(Category, slug=slug)
    
    # Get all articles for this category
    articles_list = Article.objects.filter(
        category=category
    ).order_by('-created_at')
    
    # Paginate results
    paginator = Paginator(articles_list, 9)  # 9 articles per page
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    
    # Get AdSense locations
    adsense_locations = {
        ad.name: ad.ad_code for ad in AdSenseLocation.objects.filter(is_active=True)
    }
    
    context = {
        'category': category,
        'articles': articles,
        'adsense_locations': adsense_locations,
    }
    
    return render(request, 'blog/category_articles.html', context)

def all_articles(request):
    articles_list = Article.objects.order_by('-created_at')
    
    paginator = Paginator(articles_list, 9)  # 9 articles per page
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    
    # Get AdSense locations
    adsense_locations = {
        ad.name: ad.ad_code for ad in AdSenseLocation.objects.filter(is_active=True)
    }
    
    context = {
        'articles': articles,
        'adsense_locations': adsense_locations,
    }
    
    return render(request, 'blog/all_articles.html', context)

def bmi_calculator(request):
    # Get AdSense locations
    adsense_locations = {
        ad.name: ad.ad_code for ad in AdSenseLocation.objects.filter(is_active=True)
    }
    
    context = {
        'adsense_locations': adsense_locations,
    }
    
    return render(request, 'blog/bmi_calculator.html', context)

# @csrf_exempt # Removed csrf_exempt
def subscribe_newsletter(request):
    if request.method == 'POST':
        client_ip = request.META.get('REMOTE_ADDR')
        cache_key = f'newsletter_subscribe_{client_ip}'
        
        # Verifică rate limiting
        if cache.get(cache_key):
            return JsonResponse({
                'success': False, 
                'message': 'Prea multe încercări. Încearcă din nou mai târziu.'
            })
        
        email = request.POST.get('email')
        
        if not email:
            return JsonResponse({'success': False, 'message': 'Adresa de email este necesară'})
        
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'success': False, 'message': 'Adresa de email nu este validă'})
            
        # Check if subscriber already exists
        if NewsletterSubscriber.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'Această adresă de email este deja înregistrată'})
        
        # Create new subscriber
        NewsletterSubscriber.objects.create(email=email)
        
        # Setează rate limiting pentru 5 minute
        cache.set(cache_key, True, 300)
        
        return JsonResponse({'success': True, 'message': 'Te-ai abonat cu succes la newsletter!'})
    
    return JsonResponse({'success': False, 'message': 'Metoda de cerere invalidă'})
