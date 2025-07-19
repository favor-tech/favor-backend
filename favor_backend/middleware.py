import os
#Health Check
class ELBHealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.default_host = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost").split(",")[0]

    def __call__(self, request):
        if request.path == "/health/":
            request.META["HTTP_HOST"] = self.default_host
            request.is_secure = lambda: True
        return self.get_response(request)
