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

class UserProfileSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'last_login', 'password']


class FavoritesSerializer(serializers.ModelSerializer):
    full_poster_url = serializers.SerializerMethodField()
    class Meta:
        model = Favorites
        exclude = ['poster_path']
        read_only_fields = ['id']


        def get_full_poster_url(self, obj):
            client = TMDBApiClient()
            poster_url = client.get_poster_url(obj.poster_path)
            return poster_url

    