from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from ..models import User

class AuthService:
    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }

    @staticmethod
    def set_auth_cookies(response, tokens):
        response.set_cookie(
            key='access_token',
            value=tokens['access'],
            httponly=True,
            secure=False,
            samesite='Lax',
            path='/',
            max_age=3600
        )
        response.set_cookie(
            key='refresh_token',
            value=tokens['refresh'],
            httponly=True,
            secure=False,
            samesite='Lax',
            path='/',
            max_age=86400 * 7
        )
        return response

    @staticmethod
    def delete_auth_cookies(response):
        response.delete_cookie('access_token', path='/')
        response.delete_cookie('refresh_token', path='/')
        return response

    @classmethod
    def register_user(cls, validated_data):
        validated_data.pop('password_repeat', None)
        user = User.objects.create_user(**validated_data)
        return cls.get_tokens_for_user(user)

    @classmethod
    def login_user(cls, data):
        user = authenticate(email=data['email'], password=data['password'])
        
        if user is None:
            raise AuthenticationFailed("Неверный email или пароль")
        
        if not user.is_active:
            raise AuthenticationFailed("Учетная запись деактивирована")
            
        return cls.get_tokens_for_user(user)

    @staticmethod
    def logout_user(data):
        try:
            token = RefreshToken(data['refresh'])
            token.blacklist()
        except Exception:
            pass

    @classmethod
    def refresh_tokens(cls, refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
            return {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
        except Exception:
            raise AuthenticationFailed("Сессия истекла, войдите заново")