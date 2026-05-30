from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'fullname', 'avatar', 'preferred_language', 'emotional_goals', 'joined_at')
        read_only_fields = ('id', 'email', 'joined_at')

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('fullname', 'preferred_language', 'emotional_goals')
        extra_kwargs = {'fullname': {'required': False}}