from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(max_length=120, unique=True)
    username = models.CharField(max_length=150, blank=False, null=False, unique=False)
    is_active = models.BooleanField(default=False)
    active_code = models.CharField(max_length=128)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['email']
    def __str__(self):
        return self.email
    
class UserProfile(models.Model):
    GENDER_CHOICES = (
    (1, 'Male'),
    (0, 'Female'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    gender = models.IntegerField(null=True, blank=True, choices=GENDER_CHOICES)
    address = models.CharField(max_length=420, null=True, blank=True)
    mobile = models.CharField(max_length=21)
    avatar = models.ImageField(upload_to="account/%Y/%m/%d/", blank=True, null=True)
    abut_user = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.email
    