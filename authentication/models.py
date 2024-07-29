from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

#created by yashvi ghetiya
class User(AbstractUser):
    email = models.EmailField(unique=True)

class UserProfile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
   image = models.ImageField(default='default.png', upload_to='profile_pics', null=True, blank=True)
   banner_image = models.ImageField(default='default_banner.png', upload_to='banner_pics', null=True, blank=True)
   bio = models.TextField(null=True, blank=True)
   birth_date = models.DateField(null=True, blank=True)
   location = models.CharField(max_length=255, null=True, blank=True)


class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)