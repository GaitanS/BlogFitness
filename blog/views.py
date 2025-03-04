from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import Category, Article, NewsletterSubscriber, AdSenseLocation

def home(request):
    featured_article = Article.objects.filter(is_featured=True).order_by('-created_at').first()
    categories = Category.objects.all()
    
    # Get articles for each category (limited to 3 per category)
    category_articles = {}
    for category in categories:
        category_articles[category] = category.articles.order_by('-created_at')[:3]
    
    # Get AdSense locations
    adsense_locations = {
        ad.name: ad.ad_code for ad in AdSenseLocation.objects.filter(is_active=True)
    }
    
    context = {
        'featured_article': featured_article,
        'categories': categories,
        'category_articles': category_articles,
        'adsense_locations': adsense_locations,
    }
    
    return render(request, 'blog/home.html', context)

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    related_articles = Article.objects.filter(category=article.category).exclude(id=article.id).order_by('-created_at')[:3]
    
    # Get AdSense locations
    adsense_locations = {
        ad.name: ad.ad_code for ad in AdSenseLocation.objects.filter(is_active=True)
    }
    
    context = {
        'article': article,
        'related_articles': related_articles,
        'adsense_locations': adsense_locations,
    }
    
    return render(request, 'blog/article_detail.html', context)

def category_articles(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles_list = category.articles.order_by('-created_at')
    
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

@csrf_exempt
def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if not email:
            return JsonResponse({'success': False, 'message': 'Adresa de email este necesară'})
        
        # Check if subscriber already exists
        if NewsletterSubscriber.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'Această adresă de email este deja înregistrată'})
        
        # Create new subscriber
        NewsletterSubscriber.objects.create(email=email)
        
        return JsonResponse({'success': True, 'message': 'Te-ai abonat cu succes la newsletter!'})
    
    return JsonResponse({'success': False, 'message': 'Metoda de cerere invalidă'})
