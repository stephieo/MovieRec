from django.urls import path,include
from . import views

urlpatterns = [
    path('favorites/', views.UserFavoritesAPIView.as_view(), name='my-favorites'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('me/', views.UserAPIView.as_view(), name='login')
]