from rest_framework import serializers
from  services.tmdb_api_client import TMDBApiClient

class MovieSerializer(serializers.Serializer):
    """Serializer to show abridged individual movie data from TMDB API - for all movie endpoints."""
    id = serializers.IntegerField(default=0)
    adult = serializers.BooleanField()
    media_type = serializers.CharField()
    title = serializers.CharField()
    overview = serializers.CharField()
    release_date = serializers.DateField(required=False, allow_null=True)
    poster_path = serializers.CharField(required=False, allow_null=True)
    backdrop_path = serializers.CharField(required=False, allow_null=True)
    popularity = serializers.FloatField()
    genre_ids = serializers.ListField(child=serializers.IntegerField())

class TVSeriesSerializer(serializers.Serializer):
    """Serializer for abridged individual TV series data from TMDB API."""
    id = serializers.IntegerField()
    adult = serializers.BooleanField()
    media_type = serializers.CharField()
    name = serializers.CharField()
    overview = serializers.CharField()
    first_air_date = serializers.DateField(required=False, allow_null=True)
    poster_path = serializers.CharField(required=False, allow_null=True)
    backdrop_path = serializers.CharField(required=False, allow_null=True)
    popularity = serializers.FloatField()
    genre_ids = serializers.ListField(child=serializers.IntegerField())
