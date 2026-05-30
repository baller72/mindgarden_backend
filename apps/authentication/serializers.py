from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.serializers import UserSerializer

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    fullname = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'fullname', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            fullname=validated_data['fullname'],
            password=validated_data['password']
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['fullname'] = user.fullname
        token['email'] = user.email
        return token

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()