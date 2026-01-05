from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from core.permissions import IsAuthenticatedUser, IsSystemAdmin
from ..serializers.user_serializers import (
    UserMeSerializer, 
    UserUpdateSerializer, 
    UserPublicSerializer
)
from ..services.user_services import UserService

class UserMeView(APIView):
    permission_classes = [IsAuthenticatedUser]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserUpdateSerializer(data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = UserService.update_profile(request.user, serializer.validated_data)
        return Response(UserMeSerializer(user).data)

    def patch(self, request):
        return self.put(request)

    def delete(self, request):
        UserService.soft_delete(request.user)
        return Response(
            {"detail": "Account has been deactivated."}, 
            status=status.HTTP_204_NO_CONTENT
        )

class UserDetailView(APIView):
    permission_classes = [IsSystemAdmin]
    renderer_classes = [JSONRenderer]

    def get(self, request, user_id):
        user = UserService.get_user_by_id(user_id)
        
        if user == request.user:
            serializer = UserMeSerializer(user)
        else:
            serializer = UserPublicSerializer(user)
            
        return Response(serializer.data)