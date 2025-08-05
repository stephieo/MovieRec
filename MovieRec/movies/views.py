from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from services.tmdb_api_client import TMDBApiClient
from .serializers import MovieSerializer, TVSeriesSerializer


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
            
            # For TV series, we need a different serializer (they use 'name' instead of 'title')
            # For now, let's just return the raw data
            return Response(trending_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch trending TV series: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MovieDetailAPIView(APIView):
    """Get detailed information for a specific movie."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, movie_id):
        try:
            client = TMDBApiClient()
            movie_data = client.get_movie(movie_id)
            
            return Response(movie_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to fetch movie details: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# class MovieRecommendationsAPIView(APIView):
#     """Get movie recommendations based on a specific movie."""
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request, movie_id):
#         try:
#             client = TMDBApiClient()
#             recommendations_data = client.get_movie_recommendations(movie_id)
            
#             return Response(recommendations_data, status=status.HTTP_200_OK)
            
#         except Exception as e:
#             return Response(
#                 {'error': f'Failed to fetch movie recommendations: {str(e)}'}, 
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )


# class MovieSearchAPIView(APIView):
#     """Search for movies using query parameters."""
#     permission_classes = [AllowAny]
    
#     def get(self, request):
#         try:
#             # Get query parameters
#             query = request.query_params.get('query')
#             if not query:
#                 return Response(
#                     {'error': 'Query parameter is required'}, 
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
            
#             # Build search parameters
#             search_params = {
#                 'query': query,
#                 'primary_release_year': request.query_params.get('year', ''),
#                 'language': request.query_params.get('language', 'en-US'),
#                 'include_adult': request.query_params.get('include_adult', 'false').lower() == 'true'
#             }
            
#             client = TMDBApiClient()
#             search_data = client.search_movies(search_params)
            
#             return Response(search_data, status=status.HTTP_200_OK)
            
#         except Exception as e:
#             return Response(
#                 {'error': f'Failed to search movies: {str(e)}'}, 
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
