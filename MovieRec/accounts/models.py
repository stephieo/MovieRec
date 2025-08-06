from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.


class User(AbstractUser):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'password',]

    class Meta:
        db_table = 'accounts_user'
    
    email = models.EmailField(max_length= 254, unique=True)
    created_at = models.DateTimeField(auto_now_add=True) 



class Favorites(models.Model):
    class Meta: 
        db_table = 'accounts_favorites'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    tmdb_id = models.IntegerField(unique=True)
    item_name = models.CharField(max_length=250, default="null")
    poster_url = models.CharField(max_length=500, default="null")
    created_at = models.DateTimeField(auto_now_add=True)