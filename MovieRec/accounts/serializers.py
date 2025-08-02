from rest_framework import serializers
from .models import Favorites
from  services.tmdb_api_client import TMDBApiClient

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

    