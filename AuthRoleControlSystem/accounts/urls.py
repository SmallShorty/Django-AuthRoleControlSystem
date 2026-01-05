from django.urls import path

from .views.auth_views import RegisterView, LoginView, LogoutView
from .views.user_views import UserMeView, UserDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('login/', LoginView.as_view(), name='auth-login'),
    path('logout/', LogoutView.as_view(), name='auth-logout'),
    
    path('me/', UserMeView.as_view(), name='user-me'),
    path('<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
]
