from .models import Favorites, User
from .serializers import FavoritesSerializer, UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from  services.tmdb_api_client import TMDBApiClient
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

# Create your views here.

# @api_view(['GET'])
# def user_favorites(request):



class RegisterAPIView(generics.CreateAPIView):
    """
    Register a new user account.
    
    Creates a new user account with the provided credentials. The user will be able
    to log in and manage their movie/TV series favorites after successful registration.
    
    Request Body:
    - username: Unique username for the account
    - email: User's email address
    - password: Password for the account
    - first_name: User's first name (optional)
    - last_name: User's last name (optional)
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class LoginAPIView(generics.CreateAPIView):
    """
    Authenticate user credentials and log in.
    
    Validates the provided username and password combination. Upon successful
    authentication, returns a success message. JWT tokens will be implemented
    in future versions for session management.
    
    Request Body:
    - username: The user's username
    - password: The user's password
    """
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
    """
    Get current user's profile information.
    
    Returns the authenticated user's profile details including username,
    email, first name, last name, and last login timestamp.
    
    Authentication required.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserFavoritesListAPIView(generics.ListAPIView):
    """
    Get the current user's favorite movies and TV series.
    
    Returns a list of all movies and TV series that the authenticated user has
    marked as favorites. Each favorite includes the TMDB ID, item name, poster URL,
    and the date it was added to favorites.
    
    Authentication required.
    """
    # FUTURE: would be nice to categorize faves into movie and tv
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return favorites for the authenticated user only."""
        return Favorites.objects.filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        #LEARN: making custom cache key cuz django does not based on user
        cache_key = f"user_favorites_{request.user.id}"
        cached_response = cache.get(cache_key)
        
        if cached_response is not None:
            return cached_response
            
        # Get fresh data and cache it
        response = super().get(request, *args, **kwargs)
        cache.set(cache_key, response, 600)  # 10 minutes
        return response

class UserFavoritesCreateAPIView(generics.CreateAPIView):
    """
    Add a movie or TV series to the user's favorites.
    
    Adds the specified movie or TV series to the authenticated user's favorites list.
    The system automatically fetches additional details (title, poster URL) from TMDB
    and associates the favorite with the current user.
    
    Request Body:
    - tmdb_id: The TMDB ID of the movie or TV series
    - media_type: Either "movie" or "tv" to specify the content type
    
    Authentication required.
    """
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated]
    
    
    def perform_create(self, serializer):
        """Automatically associate the favorite with the current user 
           and fetch item details from TMDB.
        """
        client = TMDBApiClient()
        tmdb_id = serializer.validated_data.get('tmdb_id')
        media_type = serializer.validated_data.get('media_type')
        
        # Check if user already has this item in favorites
        if Favorites.objects.filter(
            user=self.request.user,
            tmdb_id=tmdb_id,
            media_type=media_type
        ).exists():
            raise ValidationError({
                'detail': f'You have already added this {media_type} to your favorites.',
                'tmdb_id': tmdb_id,
                'media_type': media_type
            })
        
        if media_type == "movie":
            item_details = client.get_movie(tmdb_id)
            item_name = item_details.get("title")  
        else:  # media_type == "tv"
            item_details = client.get_series(tmdb_id)
            item_name = item_details.get("name")  
        
        # construct poster url
        poster_path = item_details.get("poster_path")
        poster_url = client.get_poster_url(poster_path)

        
        serializer.save(
            user=self.request.user,
            item_name=item_name,
            poster_url=poster_url,
            media_type=media_type
        )
        
        # cache invalidation on addition of new fave
        cache_key = f"user_favorites_{self.request.user.id}"
        cache.delete(cache_key)


class UserFavoritesDeleteAPIView(generics.DestroyAPIView):
    """
    Remove a movie or TV series from the user's favorites.
    
    Removes the specified movie or TV series from the authenticated user's favorites
    list using the TMDB ID. Only the user who added the favorite can remove it.
    
    Path Parameters:
    - tmdb_id: The TMDB ID of the favorite to remove
    
    Authentication required.
    """
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'tmdb_id'  # Use tmdb_id instead of pk for lookup
    
    def get_queryset(self):
        """Only allow users to delete their own favorites."""
        return Favorites.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        favorite = self.get_object()
        item_name = favorite.item_name
        self.perform_destroy(favorite)
        
        # cache invalidation when user removes a fave
        cache_key = f"user_favorites_{self.request.user.id}"
        cache.delete(cache_key)
        
        return Response(
            {'message': f'Favorite "{item_name}" removed successfully'}, 
            status=status.HTTP_200_OK
        )