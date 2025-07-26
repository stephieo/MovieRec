import requests
# import environ
# import os
# from pathlib import Path
from django.conf import settings

# # Build paths like Django does
# BASE_DIR = Path(__file__).resolve().parent.parent

# env = environ.Env()

# # Read the .env file from the project root
# environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

#TODO: request error handling
class TMDBApiClient:
    """client to interact with the TMDB API"""
    def __init__(self):
        """API key, base url and auth header for all requests"""
        self.api_access_token = settings.TMDB_TOKEN
        self.base_url = "https://api.themoviedb.org/3"
        self.auth_header =  f"Bearer {self.api_access_token}"

    def get_trending_movies(self):
        """"get the weekly list of trending movies"""

        url = f"{self.base_url}/trending/movie/week"
        headers = {
            "accept":  "application/json",
            "Authorization": self.auth_header
        }

        response = requests.get(url, headers=headers)
        return response.json()
    
    def get_trending_series(self):
        """Get weekly list of trending series"""
        url = f"{self.base_url}/trending/tv/week"
        headers = {
            "accept":  "application/json",
            "Authorization": self.auth_header
        }

        response = requests.get(url, headers=headers)
        return response.json()

    def search_movies(self):
        pass
    
    def search_series(self):
        pass
    
    def get_movie(self, movie_id):
        """Get detailed information for a specific movie.
        
        Args:
            movie_id (int): The TMDB movie ID.
            
        Returns:
            str: JSON response containing movie details.
            
        Raises:
            requests.RequestException: If the API request fails.
        """
        url = f"{self.base_url}/movie/{movie_id}"
        headers = {
            "accept":  "application/json",
            "Authorization": self.auth_header
        }

        response = requests.get(url, headers=headers)
        return response.json()


    def get_recommendations(self):
        pass


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
    print(f"API Token loaded: {client.api_access_token[:10]}...")  # Only show first 10 chars for security
    # print(client.get_movie(617126))
    print(client.get_trending_movies())