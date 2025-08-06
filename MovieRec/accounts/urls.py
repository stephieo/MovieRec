from django.urls import path,include
from . import views

urlpatterns = [
    path('favorites/', views.UserFavoritesListAPIView.as_view(), name='my-favorites'),
    path('favorites/add/', views.UserFavoritesCreateAPIView.as_view(), name='add-favorite'),
    path('favorites/delete/<int:tmdb_id>/', views.UserFavoritesDeleteAPIView.as_view(), name='remove-favorite'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('me/', views.UserAPIView.as_view(), name='login')
]