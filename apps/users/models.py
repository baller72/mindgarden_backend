from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from apps.users.manager import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    fullname = models.CharField(max_length=150)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    # timezone = models.CharField(max_length=50, default='UTC')
    preferred_language = models.CharField(max_length=10, default='en')
    emotional_goals = models.TextField(blank=True, default='')
    joined_at = models.DateTimeField(auto_now_add=timezone.now())

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    def __str__(self):
        return self.email