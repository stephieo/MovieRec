from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from services.tmdb_api_client import TMDBApiClient
from .serializers import MovieSerializer, TVSeriesSerializer, MovieDetailSerializer, TVDetailSerializer


class TrendingMoviesAPIView(APIView):
    """Get trending movies (weekly)."""
    permission_classes = [IsAuthenticated]
    
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
    """Get weekly trending TV series from TMDB API."""
    permission_classes = [IsAuthenticated]
    
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
    """search for a movie with query"""
    permission_classes = [IsAuthenticated]
    
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
            
            # Build search parameters
            search_params = {
                'query': query,
                'primary_release_year': request.query_params.get('year', ''),
                'language': request.query_params.get('language', 'en-US'),
                'include_adult': request.query_params.get('include_adult', 'false').lower() == 'true'
            }
            search_results = client.search_movies(search_params)
            
            # abridge the results from TMDB with serializer
            movies = search_results.get('results', [])
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
    """search for a tv series with query"""
    permission_classes = [IsAuthenticated]
    
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
            
            # Build search parameters
            search_params = {
                'query': query,
                'first_air_date_year': request.query_params.get('year', ''),
                'language': request.query_params.get('language', 'en-US'),
                'include_adult': request.query_params.get('include_adult', 'false').lower() == 'true'
            }

            search_results = client.search_series(search_params)
            
            # abridge the results from TMDB with serializer
            series = search_results.get('results', [])
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
    """Get detailed information for a specific movie."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, tmdb_id):
        try:
            client = TMDBApiClient()
            movie_data = client.get_movie(tmdb_id)
            movie_data["media_type"] = "movie"
            serializer = MovieDetailSerializer(movie_data)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch movie details: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class TVDetailAPIView(APIView):
    """Get detailed information for a specific tv series."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, tmdb_id):
        try:
            client = TMDBApiClient()
            series_data = client.get_series(tmdb_id)
            series_data["media_type"] = "series"
            serializer = TVDetailSerializer(series_data)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch series details: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class MovieRecommendationsAPIView(APIView):
    """Get movie recommendations based on a specific movie."""
    permission_classes = [IsAuthenticated]
    
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


# class MovieSearchAPIView(APIView):
#     """Search for movies using query parameters."""
#     permission_classes = [AllowAny]
    
#     def get(self, request):
#         try:
            
#             client = TMDBApiClient()
#             search_data = client.search_movies(search_params)
            
#             return Response(search_data, status=status.HTTP_200_OK)
            
#         except Exception as e:
#             return Response(
#                 {'error': f'Failed to search movies: {str(e)}'}, 
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
