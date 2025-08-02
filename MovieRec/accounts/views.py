from .models import Favorites, User
from .serializers import FavoritesSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Responce
# Create your views here.

@api_view(['GET'])
def user_favorites(request):
    favorites = Favorites.objects.filter(user_id=request.user)
    serializer = FavoritesSerializer(favorites, many=True)
    return  Responce(serializer.data)
