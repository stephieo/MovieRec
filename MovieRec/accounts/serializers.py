from rest_framework import serializers
from .models import Favorites, User
from  services.tmdb_api_client import TMDBApiClient

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email' ]
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'last_login', 'email']

class FavoritesSerializer(serializers.ModelSerializer):
    media_type = serializers.ChoiceField(choices=['movie', 'tv'], write_only=True, help_text="Content type: 'movie' or 'tv'")
    
    class Meta:
        model = Favorites
        fields = ['id', 'tmdb_id', 'item_name', 'poster_url', 'created_at', 'media_type']
        read_only_fields = ['id', 'item_name', 'poster_url', 'created_at'] #LEARN: this means  the client doesnt need to provide this in the request
    
    def create(self, validated_data):
        # Remove media_type since it's not a field in the Favorites model
        validated_data.pop('media_type', None)
        return super().create(validated_data) 

    