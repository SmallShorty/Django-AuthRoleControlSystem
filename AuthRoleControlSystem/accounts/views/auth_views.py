from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer

from ..serializers.auth_serializers import RegisterSerializer, LoginSerializer
from ..services.auth_service import AuthService

class RegisterView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        tokens = AuthService.register_user(serializer.validated_data)
        response = Response(
            {"detail": "User has been successfully registered"},
            status=status.HTTP_201_CREATED
        )
        return AuthService.set_auth_cookies(response, tokens)

class LoginView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            tokens = AuthService.login_user(serializer.validated_data)
            response = Response({
                "status": "success",
                "message": "Logged in",
            }, status=status.HTTP_200_OK)
            
            return AuthService.set_auth_cookies(response, tokens)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        
        AuthService.logout_user({'refresh': refresh_token})
        
        response = Response(
            {"detail": "Logout"}, 
            status=status.HTTP_200_OK
        )
            
        return AuthService.delete_auth_cookies(response)

class TokenRefreshView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        
        tokens = AuthService.refresh_tokens(refresh_token)
        response = Response(
            {"detail": "Tokens are refreshed"}, 
            status=status.HTTP_200_OK
        )
        return AuthService.set_auth_cookies(response, tokens)