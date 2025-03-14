from django.http import HttpResponsePermanentRedirect

class WwwRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().lower()
        if host == "ghidfit.ro":
            new_url = request.build_absolute_uri().replace("ghidfit.ro", "www.ghidfit.ro", 1)
            return HttpResponsePermanentRedirect(new_url)
        return self.get_response(request)

class SitemapContentTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path == '/sitemap.xml':
            response['Content-Type'] = 'application/xml; charset=utf-8'
        return response






