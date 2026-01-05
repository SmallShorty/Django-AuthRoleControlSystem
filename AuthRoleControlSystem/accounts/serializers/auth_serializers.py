from rest_framework import serializers
from ..models import User

class RegisterSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'middle_name', 'password', 'password_repeat']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password_repeat']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return data

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()