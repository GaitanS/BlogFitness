# Cod comentat deoarece redirecționarea este gestionată de Cloudflare
"""
from django.http import HttpResponsePermanentRedirect

class WwwRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().lower()
        if host == 'ghidfit.ro':
            return HttpResponsePermanentRedirect(
                'https://www.ghidfit.ro' + request.path
            )
        return self.get_response(request)
"""

class SitemapContentTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path == '/sitemap.xml':
            response['Content-Type'] = 'application/xml; charset=utf-8'
        return response


