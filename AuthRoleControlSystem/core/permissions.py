from rest_framework.permissions import BasePermission
from authorization.models import AccessRoleRule

class IsAuthenticatedUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

class IsSystemAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.roles.filter(slug='admin').exists()
    
class HasRole(BasePermission):
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.roles.filter(slug__in=self.allowed_roles).exists()

def role_required(*roles):
    class DataDrivenRolePermission(HasRole):
        def __init__(self):
            super().__init__(roles)
    return DataDrivenRolePermission

class HasElementPermission(BasePermission):
    def __init__(self, element_slug, permission_type):
        self.element_slug = element_slug
        self.permission_type = permission_type

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
            
        if request.user.roles.filter(slug='admin').exists():
            return True

        return AccessRoleRule.objects.filter(
            role__in=request.user.roles.all(),
            element__slug=self.element_slug,
            **{self.permission_type: True}
        ).exists()

def can_do(element_slug, permission_type):
    class DynamicPermission(HasElementPermission):
        def __init__(self):
            super().__init__(element_slug, permission_type)
    return DynamicPermission