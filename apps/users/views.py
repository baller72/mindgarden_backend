from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer, UserUpdateSerializer
from .permissions import IsOwner

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return UserUpdateSerializer
        return UserSerializer