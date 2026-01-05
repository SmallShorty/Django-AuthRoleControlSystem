from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch

from .models import Role, BusinessElement, AccessRoleRule
from .serializers import RoleSerializer, BusinessElementDetailSerializer

class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RoleSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Role.objects.prefetch_related(
            Prefetch(
                'accessrolerule_set',
                queryset=AccessRoleRule.objects.select_related('element')
            )
        ).all()

class BusinessElementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BusinessElementDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return BusinessElement.objects.prefetch_related(
            Prefetch(
                'accessrolerule_set',
                queryset=AccessRoleRule.objects.select_related('role')
            )
        ).all()

class UserRolesDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = request.user.roles.prefetch_related(
            Prefetch(
                'accessrolerule_set', 
                queryset=AccessRoleRule.objects.select_related('element')
            )
        ).all()
        
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)