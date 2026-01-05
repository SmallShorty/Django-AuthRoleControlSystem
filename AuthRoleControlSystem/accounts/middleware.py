from django.utils.deprecation import MiddlewareMixin
from .services.auth_service import AuthService

class TokenRefresh(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')
        
        if not access_token and refresh_token:
            try:
                tokens = AuthService.refresh_tokens(refresh_token)
                request._new_tokens = tokens
            except:
                pass

    def process_response(self, request, response):
        if hasattr(request, '_new_tokens'):
            AuthService.set_auth_cookies(response, request._new_tokens)
        return response