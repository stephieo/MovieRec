from rest_framework import serializers
from  services.tmdb_api_client import TMDBApiClient

class MovieSerializer(serializers.Serializer):
    """Serializer to show abridged individual movie data for trending/search results."""
    id = serializers.IntegerField(default=0)
    adult = serializers.BooleanField()
    media_type = serializers.CharField() # this is necessary for control flow in favorites creation
    title = serializers.CharField()
    overview = serializers.CharField()
    release_date = serializers.DateField(required=False, allow_null=True)
    poster_path = serializers.CharField(required=False, allow_null=True)
    backdrop_path = serializers.CharField(required=False, allow_null=True)
    popularity = serializers.FloatField()
    genre_ids = serializers.ListField(child=serializers.IntegerField())

class MovieDetailSerializer(serializers.Serializer):
    """Serializer for detailed movie data for movie details endpoint."""
    id = serializers.IntegerField()
    adult = serializers.BooleanField()
    media_type = serializers.CharField() # this is necessary for control flow in favorites creation
    title = serializers.CharField()
    overview = serializers.CharField()
    release_date = serializers.DateField(required=False, allow_null=True)
    poster_path = serializers.CharField(required=False, allow_null=True)
    backdrop_path = serializers.CharField(required=False, allow_null=True)
    popularity = serializers.FloatField()
    tagline = serializers.CharField(required=False, allow_null=True)
    genres = serializers.ListField(child=serializers.DictField()) #NOTE: genres here is an array of dicts/objects, not just IDs 


class TVDetailSerializer(serializers.Serializer):
    """Serializer for detailed tv data for tv details endpoint."""
    id = serializers.IntegerField()
    adult = serializers.BooleanField()
    media_type = serializers.CharField() # this is necessary for control flow in favorites creation
    name = serializers.CharField()
    overview = serializers.CharField()
    first_air_date = serializers.DateField(required=False, allow_null=True)
    no_of_seasons = serializers.IntegerField(default=1) # this should be a computed count of the list gotten
    poster_path = serializers.CharField(required=False, allow_null=True)
    backdrop_path = serializers.CharField(required=False, allow_null=True)
    popularity = serializers.FloatField()
    tagline = serializers.CharField(required=False, allow_null=True)
    genres = serializers.ListField(child=serializers.DictField()) #NOTE: genres here is an array of dicts/objects, not just IDs 


class TVSeriesSerializer(serializers.Serializer):
    """Serializer for abridged individual TV series data  for trending/search results."""
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
