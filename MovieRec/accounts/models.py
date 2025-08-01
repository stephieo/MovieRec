from django.db import models
from django.contrib.auth.models import AbstractUser 
# Create your models here.


class User(AbstractUser):
    pass


class Favorites(models.Models):
    id = models.UUIDField(primary_key=true, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='favorites')
    tmdb_id = models.IntegerField(unique=True, max_digits=10)
    created_at models.DateTimeField(auto_now_add=True)