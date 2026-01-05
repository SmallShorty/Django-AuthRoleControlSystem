from rest_framework import serializers
from .models import Role, BusinessElement, AccessRoleRule
from .constants import PERMISSION_FIELDS

class ActionPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRoleRule
        fields = PERMISSION_FIELDS

class AllowedActionSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='element.name')
    slug = serializers.ReadOnlyField(source='element.slug')
    permissions = ActionPermissionSerializer(source='*')

    class Meta:
        model = AccessRoleRule
        fields = ['name', 'slug', 'permissions']

class RoleSerializer(serializers.ModelSerializer):
    allowed_actions = AllowedActionSerializer(
        source='accessrolerule_set', 
        many=True, 
        read_only=True
    )

    class Meta:
        model = Role
        fields = ['name', 'slug', 'allowed_actions']

class RoleShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name', 'slug']

class ElementRoleAccessSerializer(serializers.ModelSerializer):
    role = RoleShortSerializer(read_only=True)
    permissions = ActionPermissionSerializer(source='*')

    class Meta:
        model = AccessRoleRule
        fields = ['role', 'permissions']

class BusinessElementDetailSerializer(serializers.ModelSerializer):
    allowed_roles = ElementRoleAccessSerializer(
        source='accessrolerule_set', 
        many=True, 
        read_only=True
    )

    class Meta:
        model = BusinessElement
        fields = ['name', 'slug', 'description', 'allowed_roles']
        
        