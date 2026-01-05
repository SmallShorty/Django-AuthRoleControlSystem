from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    roles = models.ManyToManyField(
        'authorization.Role', 
        through='authorization.UserRole',
        related_name='users',
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name}" + (f" {self.middle_name}" if self.middle_name else "")
