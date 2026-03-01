from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    bio = models.TextField(blank=True, null=True)
    area_of_expertise = models.CharField(max_length=30, default="General")
    picture = models.ImageField(upload_to='users/', blank=True, null=True)
    is_influencer = models.BooleanField(default=False)
    id_card_face = models.ImageField(upload_to='card_face/', blank=True, null=True)
    id_card_back = models.ImageField(upload_to='card_back/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
