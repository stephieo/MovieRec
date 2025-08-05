from django.urls import path,include
from . import views


urlpatterns = [
    path('trending/movies/', views.TrendingMoviesAPIView.as_view(), name='trending_movies_weekly'),
    path('trending/tv/', views.TrendingTVAPIView.as_view(), name='trending_tvseries_weekly'),
    path('<int:tmdb_id>/', views.MovieDetailAPIView.as_view(), name='movie_details'),
]