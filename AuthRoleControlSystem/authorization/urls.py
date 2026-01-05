from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import BusinessElementViewSet, RoleViewSet, UserRolesDetailView

router = SimpleRouter()
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'business-elements', BusinessElementViewSet, basename='business-element')

urlpatterns = [
    path('my-roles/', UserRolesDetailView.as_view(), name='user-roles-detail'),
    path('', include(router.urls)),
]