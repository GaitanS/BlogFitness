from django.http import HttpResponsePermanentRedirect

class WwwRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().lower()
        if not host.startswith('www.') and not host.startswith('localhost'):
            return HttpResponsePermanentRedirect(
                f'https://www.{host}{request.path}'
            )
        return self.get_response(request)

class SitemapContentTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path == '/sitemap.xml':
            response['Content-Type'] = 'application/xml; charset=utf-8'
        return response



