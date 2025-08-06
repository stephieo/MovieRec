from django.urls import path,include
from . import views


urlpatterns = [
    path('trending/movies/', views.TrendingMoviesAPIView.as_view(), name='trending_movies_weekly'),
    path('trending/tv/', views.TrendingTVAPIView.as_view(), name='trending_tvseries_weekly'),
    path('search/movies/', views.SearchMoviesAPIView.as_view(), name='search_movies'),
    path('search/tv/', views.SearchTVAPIView.as_view(), name='search_tv'),
    path('<int:tmdb_id>/', views.MovieDetailAPIView.as_view(), name='movie_detail'),
    path('tv/<int:tmdb_id>/', views.TVDetailAPIView.as_view(), name='tv_detail'),
    path('recommendations/<int:tmdb_id>/', views.MovieRecommendationsAPIView.as_view(), name='movie_recommendations'),
    path('recommendations/tv/<int:tmdb_id>/', views.TVRecommendationsAPIView.as_view(), name='tv_recommendations'),
]