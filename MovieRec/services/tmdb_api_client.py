import requests

from django.conf import settings
from typing import TypedDict, NotRequired


class MovieSearchParams(TypedDict):
    query: str
    primary_release_year: str
    language: NotRequired[str]
    include_adult: NotRequired[bool] 

class SearchParams(TypedDict):
    query: str
    primary_release_year: str
    language: NotRequired[str]
    include_adult: NotRequired[bool] 

#TODO: request error handling

class TMDBApiClient:
    """Client to interact with The Movie Database (TMDB) API.
    
    This class provides methods to fetch movie and TV series data from TMDB,
    including trending content, search functionality, and recommendations.
    """
    
    def __init__(self):
        """Client initialization.
        
        Set up the API access token, base URL, and authorization header
        for all API requests.
        """
        self.api_access_token = settings.TMDB_TOKEN
        self.base_url = "https://api.themoviedb.org/3"
        self.auth_header =  f"Bearer {self.api_access_token}"

    def get_trending_movies(self):
        """Get the weekly list of trending movies.
        
        Returns:
            dict: JSON response containing trending movies data.
            
        Raises:
            requests.RequestException: If the API request fails.
        """

        url = f"{self.base_url}/trending/movie/week"
        headers = {
            "accept":  "application/json",
            "Authorization": self.auth_header
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    
    def get_trending_series(self):
        """Get the weekly list of trending TV series.
        
        Returns:
            dict: JSON response containing trending TV series data.
            
        Raises:
            requests.RequestException: If the API request fails.
        """
        url = f"{self.base_url}/trending/tv/week"
        headers = {
            "accept":  "application/json",
            "Authorization": self.auth_header
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()

    def search_movies(self, params_dict: MovieSearchParams) -> dict:
        """Search for movies using a query string.
        
        Args:
            param_dict (dict): Dictionary containing search parameters for the API request.
            Expected keys:
            - query (str): The search query string for TV series titles.
            - primary_release_year (str): The primary release year of the movie.
            - language (str, optional): Language code (e.g., 'en-US'). Defaults to 'en-US'.
            - include_adult (bool, optional): Include adult content. Defaults to False.
        
        Returns:
            dict: JSON response containing search results for movies.
            
        Raises:
            requests.RequestException: If the API request fails.
            
        """
        url = f"{self.base_url}/search/movie"
        headers = {
            "accept":  "application/json",
            "Authorization": self.auth_header
        }

        response = requests.get(url, headers=headers, params=params_dict)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    
    def search_series(self, params_dict):
        """Search for TV series using a query string.
        
        Args:
            param_dict (dict): Dictionary containing search parameters for the API request.
            Expected keys:
            - query (str): The search query string for TV series titles.
            - first_air_date_year (str, optional): The first air date year of the series.
            - year (str, optional): The any episode air date of series.
            - language (str, optional): Language code (e.g., 'en-US'). Defaults to 'en-US'.
            - include_adult (bool, optional): Include adult content. Defaults to False.

        Returns:
            dict: JSON response containing search results for TV series.
            
        Raises:
            requests.RequestException: If the API request fails.
            
        """
        url = f"{self.base_url}/search/tv"
        headers = {
            "accept":  "application/json",
            "Authorization": self.auth_header
        }

        response = requests.get(url, headers=headers, params=params_dict)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    
    def get_movie(self, movie_id: int) -> dict:
        """Get detailed information for a specific movie.
        
        Args:
            movie_id (int): The TMDB movie ID.
            
        Returns:
            dict: JSON response containing movie details.
            
        Raises:
            requests.RequestException: If the API request fails.
        """
        if not isinstance(movie_id, int) or movie_id <= 0:
            raise ValueError(f"movie_id must be a positive integer")

        url = f"{self.base_url}/movie/{movie_id}"
        headers = {
            "accept":  "application/json",
            "Authorization": self.auth_header
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()

    def get_series(self, series_id: int) -> dict:
        """Get detailed information for a specific tv series.
        
        Args:
            series_id (int): The TMDB movie ID.
            
        Returns:
            dict: JSON response containing series details.
            
        Raises:
            requests.RequestException: If the API request fails.
        """
        if not isinstance(series_id, int) or series_id <= 0:
            raise ValueError(f"series_id must be a positive integer")
    
        url = f"{self.base_url}/movie/{series_id}"
        headers = {
            "accept":  "application/json",
            "Authorization": self.auth_header
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()

    def get_movie_recommendations(self, movie_id: int) -> dict:
        """Get movie recommendations based on a specific movie.
        
        Args:
            movie_id (int): The TMDB movie ID to get recommendations for.
            
        Returns:
            dict: JSON response containing recommended movies.
            
        Raises:
            requests.RequestException: If the API request fails.
            
        """

        if not isinstance(movie_id, int) or movie_id <= 0:
            raise ValueError(f"movie_id must be a positive integer")
                                    
        url = f"{self.base_url}/movie/{movie_id}/recommendations"
        headers = {
            "accept":  "application/json",
            "Authorization": self.auth_header
        }

        response = requests.get(url, headers=headers)
        #FUTURE: add custom logic to filter and return only movies with the same genre tag
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()

    def get_series_recommendations(self, series_id: int) -> dict:
        """Get TV series recommendations based on a specific series.
        
        Args:
            series_id (int): The TMDB TV series ID to get recommendations for.
            
        Returns:
            dict: JSON response containing recommended TV series.
            
        Raises:
            requests.RequestException: If the API request fails.
            
        Todo:
            Add custom logic to filter and return only series with the same genre tag.
        """
        url = f"{self.base_url}/tv/{series_id}/recommendations"
        headers = {
            "accept":  "application/json",
            "Authorization": self.auth_header
        }

        response = requests.get(url, headers=headers)
        #FUTURE: add custom logic to filter and return only series with the same genre tag
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()

    def get_poster_url(self, poster_path:str) -> str:
        if poster_path == "null":
            url = f"https://placehold.co/185x280?text=No+Image+Found&font=playfair+display"
        
        url = f"{self.base_url}/t/p/w185/{poster_path}."
        return url
    

if __name__ == "__main__":
    # Setup Django only when running standalone for testing
    import os
    import sys
    import django
    from pathlib import Path
    
    # adding project root to Python path so core module can be found
    project_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(project_root))
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()
    
    client = TMDBApiClient()
    # print(f"API Token loaded: {client.api_access_token[:10]}...")  # Only show first 10 chars for security
    # print(client.get_movie(617126))
    # print(client.get_trending_movies())
    # print(client.get_movie_recommendations(617126))
    