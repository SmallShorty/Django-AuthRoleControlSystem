from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from ..models import User

class UserService:
    @staticmethod
    def get_user_profile(user):
        return 
    
    @staticmethod
    def get_user_by_id(user_id):
        from django.shortcuts import get_object_or_404
        return get_object_or_404(User, id=user_id)
    
    @staticmethod
    def update_profile(user, data):
        for attr, value in data.items():
            setattr(user, attr, value)
        user.save()
        return user
    
    @staticmethod
    def soft_delete(user):
        user.is_active = False
        user.save()