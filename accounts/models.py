from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    channels_created = models.PositiveIntegerField(default=0)
    user_icon = models.ImageField(upload_to='images/icon', blank=True, default='images/icon/default-icon.png')
