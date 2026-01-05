from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from accounts.models import User
from .models import Role, BusinessElement, AccessRoleRule, UserRole
from .constants import PERMISSION_FIELDS
from django.db import transaction

class AuthorizationService:
    @staticmethod
    @transaction.atomic
    def create_role_with_permissions(name, permissions_data):
        role = Role.objects.create(
            name=name, 
            slug=slugify(name)
        )
        
        for item in permissions_data:
            element_slug = item.get('slug')
            element = get_object_or_404(BusinessElement, slug=element_slug)
            
            perm_values = {
                field: item.get(field, False) 
                for field in AuthorizationService.PERMISSION_FIELDS
            }
            
            AccessRoleRule.objects.create(
                role=role,
                business_element_id=element.id,
                **perm_values
            )
        return role
    
    @staticmethod
    def set_role_permissions(role_id, element_slug, permissions_list):
        role = get_object_or_404(Role, pk=role_id)
        element = get_object_or_404(BusinessElement, name=element_slug)
        
        defaults = {field: (field in permissions_list) for field in PERMISSION_FIELDS}
        
        rule, _ = AccessRoleRule.objects.update_or_create(
            role=role,
            element=element,
            defaults=defaults
        )
        return rule

    @staticmethod
    def assign_role(user_id, role_slug):
        user = get_object_or_404(User, pk=user_id)
        role = get_object_or_404(Role, slug=role_slug)
        user_role, created = UserRole.objects.get_or_create(
                    user=user, 
                    role=role
                )
        return user_role, created

    @staticmethod
    def remove_role(user_id, role_slug):
        user = get_object_or_404(User, pk=user_id)
        role = get_object_or_404(Role, slug=role_slug)
        deleted_count, _ = UserRole.objects.filter(
                    user=user, 
                    role=role
                ).delete()
                
        return deleted_count > 0

    @staticmethod
    def get_grouped_element_permissions(element):
        rules = AccessRoleRule.objects.filter(element=element).select_related('role')
        grouped_data = {field: [] for field in PERMISSION_FIELDS}

        for rule in rules:
            for field in PERMISSION_FIELDS:
                if getattr(rule, field):
                    grouped_data[field].append({
                        'role_id': rule.role.id,
                        'role_name': rule.role.name,
                        'role_slug': rule.role.slug
                    })
        return grouped_data