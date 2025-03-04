from .models import Category, AdSenseLocation

def global_context(request):
    # Get all categories
    categories = Category.objects.all()
    
    # Get AdSense locations
    adsense_locations = {
        ad.name: ad.ad_code for ad in AdSenseLocation.objects.filter(is_active=True)
    }
    
    return {
        'categories': categories,
        'adsense_locations': adsense_locations
    }