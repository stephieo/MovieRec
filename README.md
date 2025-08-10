# MovieRec

A high-performance backend API for movie and TV series discovery, built with Django REST Framework and powered by The Movie Database (TMDB).

## 🎬 Live Demo
- **live Interactive API Documentation**: [https://movierec-6usy.onrender.com](https://movierec-6usy.onrender.com)

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Project Documentation](#project-documentation)
- [Examples](#examples)
- [Authors](#authors)


## Description

MovieRec is an MVP high-performing backend API for a movie recommendation platform. Built with Django REST Framework, it provides comprehensive RESTful APIs for movie and TV series discovery, user authentication, and personalized favorites management. 

The system integrates with The Movie Database (TMDB) API to deliver real-time entertainment content data, implements Redis caching for optimal performance, and features comprehensive API documentation through Swagger UI.

**Key Highlights:**

- 🎬 **Real-time TMDB Integration** for movies and TV series data  
- ⚡ **Redis Caching** for high-performance API responses
- 🔐 **JWT Authentication** for secure user management
- 📚 **Interactive Swagger Documentation** for easy API testing
- 🐳 **Docker Containerized**  Complete containerization for easy  seamless development and deployment


## Features

### 🎬 Movie & TV Series Discovery
- **Trending Content**: Get weekly trending movies and TV series from TMDB
- **Advanced Search**: Search movies and TV series with query parameters and filters
- **Detailed Information**: Complete metadata including cast, ratings, release dates, and synopses
- **Smart Recommendations**: AI-powered recommendations based on TMDB algorithms
- **Content Categories**: Support for both movies and TV series with type-specific handling

### 👤 User Management & Authentication
- **Secure Registration**: User account creation with email validation
- **JWT Authentication**: Token-based authentication for secure API access
- **User Profiles**: Comprehensive user profile management
- **Session Management**: Secure login/logout functionality

### ⭐ Personal Favorites System
- **Add/Remove Favorites**: Save movies and TV shows to personal favorites list
- **Duplicate Prevention**: Smart validation prevents duplicate favorites
- **Media Type Support**: Separate handling for movies vs TV series favorites
- **Personalized Lists**: View and manage individual user favorites

### 🚀 Performance & Architecture
- **Redis Caching**: caching system for frequently accessed data
  - User favorites cached for 10 minutes with smart invalidation
  - TMDB API responses cached to reduce external API calls
- **RESTful Design**: API endpoints following REST principles  
- **Error Handling**: Comprehensive error responses with detailed messages


### 📖 Developer Experience
- **Interactive Documentation**: Full Swagger/OpenAPI documentation with testing interface
- **Docker Support**: Complete containerization for easy development and deployment
- **Environment Configuration**: Flexible environment-based configuration management

## Technologies Used

| Category | Technology | Description |
|----------|------------|-------------|
| **Backend** | Python 3.12 | Modern runtime |
| | Django 5.2.4 | Web framework |
| | Django REST Framework | API toolkit |
| **Database** | PostgreSQL | Primary database |
| | Redis | Caching layer |
| | django-redis | Cache integration |
| **External APIs** | TMDB API | Movie data |
| | Custom Client | API integration |
| **Authentication** | Django Auth | User management |
| | Custom User | Extended functionality |
| **Documentation** | drf-yasg | Swagger generation |
| | Swagger UI | Interactive testing |
| **Deployment** | Docker | Containerization platform |
| | Render | Cloud hosting |
| | Gunicorn | Production server |

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
touch .env
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


#### **Authentication Flow**
```bash
# Register a new user
curl -X POST "https://movierec-6usy.onrender.com/api/accounts/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "moviefan",
    "email": "fan@example.com", 
    "password": "securepass123",
    "first_name": "Movie",
    "last_name": "Fan"
  }'

# Login to get access token
curl -X POST "https://movierec-6usy.onrender.com/api/accounts/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "moviefan",
    "password": "securepass123"
  }'
```
#### **Test the Live API**
```bash
# Get trending movies 
curl "https://movierec-6usy.onrender.com/api/movies/trending/movies/"

# Search for movies
curl "https://movierec-6usy.onrender.com/api/movies/search/movies/?query=batman"

# Get specific movie details
curl "https://movierec-6usy.onrender.com/api/movies/550/"
```


#### **Favorites Management (Requires Authentication)**
```bash
# Add movie to favorites
curl -X POST "https://movierec-6usy.onrender.com/api/accounts/favorites/add/" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "tmdb_id": 550,
    "media_type": "movie"
  }'

# Get user's favorites list
curl -H "Authorization: Bearer <your-token>" \
  "https://movierec-6usy.onrender.com/api/accounts/favorites/"

# Remove from favorites
curl -X DELETE -H "Authorization: Bearer <your-token>" \
  "https://movierec-6usy.onrender.com/api/accounts/favorites/delete/550/"
```
## Configuration

### Required Environment Variables
- `TMDB_API_KEY` - Your TMDB API key
- `POSTGRES_DB` - Database name  
- `POSTGRES_USER` - Database username
- `POSTGRES_PASSWORD` - Database password
- `SECRET_KEY` - Django secret key
- `REDIS_URL` - Redis connection URL

### Getting TMDB API Key
1. Visit [TMDB API](https://www.themoviedb.org/settings/api)
2. Create account and request API key
3. Add key to your `.env` file

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
- **Production**: Visit [https://movierec-6usy.onrender.com/swagger/](https://movierec-6usy.onrender.com/swagger/) for full API documentation with testing interface
- **Local Development**: Visit `http://localhost:8000/swagger/` when running locally

### API Response Examples

#### **Trending Movies Response**
```json
{
  "page": 1,
  "results": [
    {
      "id": 912649,
      "title": "Venom: The Last Dance",
      "overview": "Eddie and Venom are on the run...",
      "poster_path": "/aosm8NMQ3UyoBVpSxyimorCQykC.jpg",
      "release_date": "2024-10-22",
      "vote_average": 6.4
    }
  ],
  "total_pages": 1000,
  "total_results": 20000
}
```

#### **User Favorites Response**
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "tmdb_id": 550,
    "media_type": "movie", 
    "item_name": "Fight Club",
    "poster_url": "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
    "created_at": "2025-08-09T10:30:00Z"
  }
]
```

#### **Error Response Format**
```json
{
  "detail": "You have already added this movie to your favorites.",
  "tmdb_id": 550,
  "media_type": "movie"
}
```

## Project Documentation

For comprehensive technical documentation, visit the [`/docs`](./docs/) folder:

- **[Requirements Analysis](./docs/requirements-analysis.md)** - Detailed project requirements and specifications
- **[Database Design & ERD](./docs/database-design.md)** - Complete database schema and relationships
- **[User Stories](./docs/user-stories.md)** - User-focused feature descriptions and acceptance criteria

### Architecture Overview
The application follows a clean architecture pattern with:
- **API Layer**: Django REST Framework views handling HTTP requests/responses
- **Service Layer**: Custom TMDB API client for external data integration  
- **Data Layer**: Django ORM with PostgreSQL for persistent storage
- **Cache Layer**: Redis for performance optimization
- **Authentication Layer**: JWT-based user authentication system





## Authors

**Stephanie Olulesho** - Full Stack Developer
- GitHub: [@stephieo](https://github.com/stephieo)  
- Project Link: [https://github.com/stephieo/MovieRec](https://github.com/stephieo/MovieRec)
- Live Demo: [https://movierec-6usy.onrender.com](https://movierec-6usy.onrender.com)


Built with ❤️ using Django REST Framework and deployed on Render.
