# MovieRec
## Table of Contents
- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Examples](#examples)
- [Contributing](#contributing)
- [Testing](#testing)
- [License](#license)
- [Authors](#authors)


## Description

MovieRec is an MVP high-performing backend for a movie recommendation app. It provides RESTful APIs for movie discovery, user authentication, and favorite movie management. The system uses caching for performance optimization and demonstrates scalable backend architecture.


## Features
- **Movie & TV Series Discovery**
    - Get weekly trending movies and TV series
    - Search movies and TV series with query parameters
    - Get detailed information for specific movies/TV shows
    - Movie and TV series recommendations based on TMDB data

- **User Management & Favorites**
    - User registration and login
    - User profile management
    - Add/remove movies and TV shows to/from favorites
    - View personal favorites list

- **TMDB API Integration**
    - Real-time data from The Movie Database
    - Trending content discovery
    - Advanced search functionality
    - Detailed movie/series metadata

- **Performance & Architecture**
    - Redis caching for frequently accessed data
    - RESTful API design
    - Comprehensive error handling
    - Swagger API documentation

## Technologies Used

**Backend Framework:**
- Python 3.12
- Django REST Framework

**Database & Caching:**
- PostgreSQL
- Redis

**DevOps & Deployment:**
- Docker for containerization

**Third-party Services:**
- TMDB (The Movie Database) API

## Installation

### Prerequisites

- **Docker & Docker Compose** - For containerized development
- **Python 3.12** - Backend runtime
- **PostgreSQL** - Database (via Docker)
- **Redis** - Caching layer (via Docker)
- **TMDB API Key** - Required for movie data access

### Setup

```bash
# Clone the repository
git clone https://github.com/stephieo/MovieRec.git
cd MovieRec

# Create environment file
cp .env.example .env
# Edit .env with your TMDB API key and database credentials

# Build and start services
docker-compose up --build

# Run migrations (in a new terminal)
docker-compose exec web python manage.py migrate

# Create superuser (optional)
docker-compose exec web python manage.py createsuperuser
```

## Usage

### Starting the Application
```bash
# Start all services
docker-compose up

# Access the API documentation
http://localhost:8000/swagger/

# Test API endpoints
curl http://localhost:8000/api/movies/trending/movies/
```

### Example API Calls
```bash
# Search for movies
curl "http://localhost:8000/api/movies/search/movies/?query=batman"

# Get movie details
curl "http://localhost:8000/api/movies/550/"

# Add to favorites (requires authentication)
curl -X POST "http://localhost:8000/api/accounts/favorites/add/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"tmdb_id": 550, "type": "movie"}'
```
## Configuration

### Environment Variables
Create a `.env` file in the root directory with:

```env
# Database Configuration
POSTGRES_DB=movierec_db
POSTGRES_USER=movierec_user
POSTGRES_PASSWORD=your_secure_password

# TMDB API
TMDB_API_KEY=your_tmdb_api_key_here

# Django Settings
DEBUG=True
SECRET_KEY=your_django_secret_key

# Redis Configuration
REDIS_URL=redis://redis:6379/1
```

### Getting TMDB API Key
1. Visit [TMDB API](https://www.themoviedb.org/settings/api)
2. Create an account and request an API key
3. Add the key to your `.env` file

## API Documentation

### Authentication Endpoints
- `POST /api/accounts/register/` - User registration
- `POST /api/accounts/login/` - User login
- `GET /api/accounts/me/` - Get user profile

### Movie & TV Endpoints
- `GET /api/movies/trending/movies/` - Get trending movies
- `GET /api/movies/trending/tv/` - Get trending TV series
- `GET /api/movies/search/movies/?query=<term>` - Search movies
- `GET /api/movies/search/tv/?query=<term>` - Search TV series
- `GET /api/movies/<tmdb_id>/` - Get movie details
- `GET /api/movies/tv/<tmdb_id>/` - Get TV series details
- `GET /api/movies/recommendations/<tmdb_id>/` - Get movie recommendations

### Favorites Endpoints
- `GET /api/accounts/favorites/` - List user favorites
- `POST /api/accounts/favorites/add/` - Add to favorites
- `DELETE /api/accounts/favorites/delete/<tmdb_id>/` - Remove from favorites

### Interactive Documentation
Visit `/swagger/` when running locally for full API documentation with testing interface.



## Testing

How to run tests.
```bash
# Test Commands
```

## License

Specify the license under which this project is released.

## Authors

Stephanie Olulesho - [GitHub](https://github.com/stephieo)
