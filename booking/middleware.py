from django.conf import settings
from django.http import JsonResponse
origins = settings.CORS_ALLOWED_ORIGINS

class AuthorizedOriginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.META.get('HTTP_ORIGIN') in origins:
            return JsonResponse({'error':'You\'re not authorized to access this api'}, status=401)
        response = self.get_response(request)
        return response