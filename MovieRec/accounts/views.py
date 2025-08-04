from .models import Favorites, User
from .serializers import FavoritesSerializer, UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework import generics
from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from  services.tmdb_api_client import TMDBApiClient


# Create your views here.

# @api_view(['GET'])
# def user_favorites(request):



class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class LoginAPIView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                # tokens = RefreshToken.for_user(user)
                return Response (
                    {
                        'message': 'Login Successful',
                        # 'access': str(tokens.access_token),
                        # 'refresh': str(tokens)
                    },
                    status=status.HTTP_200_OK
                )
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserAPIView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
class UserFavoritesListAPIView(generics.ListAPIView):
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return favorites for the authenticated user only."""
        return Favorites.objects.filter(user=self.request.user)

class UserFavoritesCreateAPIView(generics.CreateAPIView):
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """Automatically associate the favorite with the current user 
           and fetch item details from TMDB.
        """
        client = TMDBApiClient()
        tmdb_id = serializer.validated_data.get('tmdb_id')
        item_type = serializer.validated_data.get('type')
        
        if item_type == "movie":
            item_details = client.get_movie(tmdb_id)
            item_name = item_details.get("title")  
        else:  # item_type == "tv"
            item_details = client.get_series(tmdb_id)
            item_name = item_details.get("name")  
        
        # construct poster url
        poster_path = item_details.get("poster_path")
        poster_url = client.get_poster_url(poster_path)

        
        serializer.save(
            user=self.request.user,
            item_name=item_name,
            poster_url=poster_url
        )

class UserFavoritesDeleteAPIView(generics.DestroyAPIView):
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'tmdb_id'  # Use tmdb_id instead of pk for lookup
    
    def get_queryset(self):
        """Only allow users to delete their own favorites."""
        return Favorites.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Favorite removed successfully'}, 
            status=status.HTTP_200_OK
        )