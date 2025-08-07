from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from services.tmdb_api_client import TMDBApiClient
from .serializers import MovieSerializer, TVSeriesSerializer, MovieDetailSerializer, TVDetailSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

# Swagger query parameters for search endpoints
QUERY_PARAM = openapi.Parameter('query', openapi.IN_QUERY, description="Search query", type=openapi.TYPE_STRING, required=True)
YEAR_PARAM = openapi.Parameter('year', openapi.IN_QUERY, description="Release/air date year (optional)", type=openapi.TYPE_STRING, required=False)
ADULT_PARAM = openapi.Parameter('include_adult', openapi.IN_QUERY, description="Include adult content (default: false)", type=openapi.TYPE_BOOLEAN, required=False, default=False)


class TrendingMoviesAPIView(APIView):
    """
    Get trending movies for the current week.
    
    Returns a paginated list of trending movies from TMDB with additional metadata
    including page information, total results, and total pages.
    """
    permission_classes = [IsAuthenticated]
    @method_decorator(cache_page(60*60*24 ,key_prefix="trending_movies")) #cache the response of this method  for 1 day
    def get(self, request):
        try:
            client = TMDBApiClient()
            trending_data = client.get_trending_movies()
            
            # abridge the results from TMDB with serializer
            movies = trending_data.get('results', [])
            serializer = MovieSerializer(movies, many=True)
            
            # full response structure
            response_data = {
                'page': trending_data.get('page', 1),
                'results': serializer.data,
                'total_pages': trending_data.get('total_pages', 1),
                'total_results': trending_data.get('total_results', 0)
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch trending movies: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TrendingTVAPIView(APIView):
    """
    Get trending TV series for the current week.
    
    Returns a paginated list of trending TV series from TMDB with additional metadata
    including page information, total results, and total pages.
    """
    permission_classes = [IsAuthenticated]
    @method_decorator(cache_page(60*60*24, key_prefix="trending_tv")) #cache the response of this method  for 1 day    
    def get(self, request):
        try:
            client = TMDBApiClient()
            trending_data = client.get_trending_series()
            
            tv_series = trending_data.get('results', [])
            serializer = TVSeriesSerializer(tv_series, many=True)
            response_data = {
                'page': trending_data.get('page', 1),
                'results': serializer.data,
                'total_pages': trending_data.get('total_pages', 1),
                'total_results': trending_data.get('total_results', 0)
            }

            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch trending TV series: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SearchMoviesAPIView(APIView):
    """
    Search for movies using a text query.
    
    Allows searching for movies by title with optional filters for release year
    and adult content inclusion. Returns paginated results matching the search criteria.
    
    Query Parameters:
    - query (required): Search term for movie titles
    - year (optional): Filter by primary release year
    - include_adult (optional): Include adult content (default: false)
    """
    permission_classes = [IsAuthenticated]
    
    @method_decorator(cache_page(60*60, key_prefix="search_movies")) #cache the response of this method  for 1 hour
    @swagger_auto_schema(manual_parameters=[QUERY_PARAM, YEAR_PARAM, ADULT_PARAM])
    def get(self, request):
        try:
            client = TMDBApiClient()

            query = request.query_params.get('query')
            if not query:
                return Response(
                    {'error': 'Query parameter is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            search_params = {
                'query': query,
                'primary_release_year': request.query_params.get('year', ''),
                'include_adult': request.query_params.get('include_adult', 'false').lower() == 'true'
            }
            search_results = client.search_movies(search_params)
            
            # abridge the results from TMDB with serializer
            movies = search_results.get('results', [])
            # Adding media_type to each result for serializer compatibility
            for movie in movies:
                movie["media_type"] = "movie"
            serializer = MovieSerializer(movies, many=True)
            
            # full response structure
            response_data = {
                'page': search_results.get('page', 1),
                'results': serializer.data,
                'total_pages': search_results.get('total_pages', 1),
                'total_results': search_results.get('total_results', 0)
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch movies search results: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SearchTVAPIView(APIView):
    """
    Search for TV series using a text query.
    
    Allows searching for TV series by title with optional filters for first air date year
    and adult content inclusion. Returns paginated results matching the search criteria.
    
    Query Parameters:
    - query (required): Search term for TV series titles
    - year (optional): Filter by first air date year
    - include_adult (optional): Include adult content (default: false)
    """
    permission_classes = [IsAuthenticated]
    
    @method_decorator(cache_page(60*60, key_prefix="search_tv"))
    @swagger_auto_schema(manual_parameters=[QUERY_PARAM, YEAR_PARAM, ADULT_PARAM])
    def get(self, request):
        try:
            client = TMDBApiClient()
            # Get query parameters
            query = request.query_params.get('query')
            if not query:
                return Response(
                    {'error': 'Query parameter is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            search_params = {
                'query': query,
                'first_air_date_year': request.query_params.get('year', ''),
                'include_adult': request.query_params.get('include_adult', 'false').lower() == 'true'
            }

            search_results = client.search_series(search_params)
            
            # abridge the results from TMDB with serializer
            series = search_results.get('results', [])
           
            # Adding media_type to each result for serializer compatibility
            for show in series:
                show["media_type"] = "tv"
            serializer = TVSeriesSerializer(series, many=True)
            
            # full response structure
            response_data = {
                'page': search_results.get('page', 1),
                'results': serializer.data,
                'total_pages': search_results.get('total_pages', 1),
                'total_results': search_results.get('total_results', 0)
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch tv search results: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MovieDetailAPIView(APIView):
    """
    Get detailed information for a specific movie.
    
    Retrieves comprehensive movie details including plot, cast, crew, ratings,
    budget, revenue, runtime, and other metadata from TMDB.
    
    Path Parameters:
    - tmdb_id: The TMDB movie ID
    """
    permission_classes = [IsAuthenticated]
    
    @method_decorator(cache_page(60*60*24*2, key_prefix="details_movie"))
    def get(self, request, tmdb_id):
        try:
            client = TMDBApiClient()
            movie_data = client.get_movie(tmdb_id)
            movie_data["media_type"] = "movie"
            serializer = MovieDetailSerializer(movie_data)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch movie details: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class TVDetailAPIView(APIView):
    """
    Get detailed information for a specific TV series.
    
    Retrieves comprehensive TV series details including plot, cast, crew, ratings,
    episode information, seasons, and other metadata from TMDB.
    
    Path Parameters:
    - tmdb_id: The TMDB TV series ID
    """
    permission_classes = [IsAuthenticated]
    
    @method_decorator(cache_page(60*60*24*2, key_prefix="detail_tb"))
    def get(self, request, tmdb_id):
        try:
            client = TMDBApiClient()
            series_data = client.get_series(tmdb_id)
            series_data["media_type"] = "tv"
            serializer = TVDetailSerializer(series_data)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch series details: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class MovieRecommendationsAPIView(APIView):
    """
    Get movie recommendations based on a specific movie.
    
    Returns a paginated list of movies similar to the specified movie,
    based on TMDB's recommendation algorithm which considers genres,
    keywords, cast, and user viewing patterns.
    
    Path Parameters:
    - tmdb_id: The TMDB movie ID to base recommendations on
    """
    permission_classes = [IsAuthenticated]
    
    @method_decorator(cache_page(60*60*2, key_prefix="recommendations_movies"))
    def get(self, request, tmdb_id):
        try:
            client = TMDBApiClient()
            recommendations_data = client.get_movie_recommendations(tmdb_id)
            
            # Serialize the recommendations data for consistency
            movies = recommendations_data.get('results', [])
            # Add media_type to each movie for serializer compatibility
            for movie in movies:
                movie["media_type"] = "movie"
            
            serializer = MovieSerializer(movies, many=True)
            
            # Return structured response like other endpoints
            response_data = {
                'page': recommendations_data.get('page', 1),
                'results': serializer.data,
                'total_pages': recommendations_data.get('total_pages', 1),
                'total_results': recommendations_data.get('total_results', 0)
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch movie recommendations: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class TVRecommendationsAPIView(APIView):
    """
    Get TV series recommendations based on a specific TV series.
    
    Returns a paginated list of TV series similar to the specified series,
    based on TMDB's recommendation algorithm which considers genres,
    keywords, cast, and user viewing patterns.
    
    Path Parameters:
    - tmdb_id: The TMDB TV series ID to base recommendations on
    """
    permission_classes = [IsAuthenticated] 
    
    @method_decorator(cache_page(60*60*2, key_prefix="recommendations_tv"))
    def get(self, request, tmdb_id):
        try:
            client = TMDBApiClient()
            recommendations_data = client.get_series_recommendations(tmdb_id)
            
            # Serialize the recommendations data for consistency
            series = recommendations_data.get('results', [])
            # Add media_type to each serie for serializer compatibility
            for serie in series:
                serie["media_type"] = "tv"
            
            serializer = TVSeriesSerializer(series, many=True)
            
            # Return structured response like other endpoints
            response_data = {
                'page': recommendations_data.get('page', 1),
                'results': serializer.data,
                'total_pages': recommendations_data.get('total_pages', 1),
                'total_results': recommendations_data.get('total_results', 0)
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch tv recommendations: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    