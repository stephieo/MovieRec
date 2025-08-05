# MovieRec Project TODO

## 🚀 Project Setup & Configuration

### Environment & Docker

- [x] Create `.env` file with database credentials
- [x] Test Docker containers startup (`docker-compose up --build`)
- [x] Verify PostgreSQL connection from Django after running migrations
- [ ] Test Redis connection and caching
- [ ] Set up Django settings for all dependencies
  - [x] `django-cors-headers==4.7.0`
  - [x] `django-environ==0.12.0`
  - [x] `django-filter==25.1`
  - [x] `django-redis==6.0.0`
  - [x] `djangorestframework==3.16.0`
  - [x] `djangorestframework_simplejwt==5.5.1`
  - [ ] `drf-nested-routers==0.94.2`
  - [x] `drf-yasg==1.21.10`
- [ ] Configure Django settings for production vs development

### Database & Models

- #FIXME [ ] Roll back migration to the beginning to alter AUTH_USER_MODEL
- [x] Design movie database schema (ERD)
- [x] Create User profile and Faves model
- [x] Run initial migrations
- [ ] Create database seed data/fixtures

## 🔐 Authentication & Authorization

### User Management (accounts app)

- [x] Implement user registration endpoint
- [x] Implement JWT login/logout endpoints
- #FUTURE[ ] Add password reset functionality
- [ ] Create user profile management
- #FUTURE[ ] Add email verification (optional)
- [ ] Implement role-based permissions (user/admin)

### User Favorites Management

- [x] Create Favorites model with TMDB integration
- [x] Implement favorites list endpoint (GET)
- [x] Implement add to favorites endpoint (POST)
- [x] Implement remove from favorites endpoint (DELETE)
- [x] Add automatic TMDB data fetching (title/name, poster)
- [x] Add content type validation (movie/tv)
- [ ] Add duplicate favorite prevention
- [ ]#FUTURE: Add favorites export functionality
- [ ]#FUTURE: Implement favorites statistics/analytics

### Security

- [ ] Configure CORS headers properly
- [ ] Add rate limiting to API endpoints
- [ ] Implement input validation and sanitization
- [ ] Add API authentication middleware

## 🎬 Core Movie Features

### Movie Management (movies app) - 🚀 SPRINT FOCUS

- [ ] Create movies app (`python manage.py startapp movies`)
- [ ] Create movie API views using TMDB client
  - [ ] TrendingMoviesAPIView
  - [ ] MovieSearchAPIView
  - [ ] MovieDetailAPIView
  - [ ] MovieRecommendationsAPIView
- [ ] Configure movie app URLs
- [ ] Add movie endpoints to main URLs
- #FUTURE[ ] Implement movie search and filtering
- #FUTURE[ ] Add genre-based filtering
- #FUTURE[ ] Create movie recommendation algorithm
- #FUTURE[ ] Add movie rating system
- #FUTURE[ ] Implement user watchlist functionality
- #FUTURE[ ] Add movie reviews and comments

### Movie Data

- [ ] Integrate with external movie API (TMDB) - [x] trending weekly movies and series - [x] movie and series search - [x] query parameter support - [x] specific movie - [x] request error handling - [ ]item id input validation ( API level?)
      -#FUTURE: [ ] recommendation filtering
      -#FUTURE: [ ] Add movie poster/image handling?

### Caching & Performance - 🚀 SPRINT FOCUS

- [ ] Implement Redis caching for TMDB API calls
  - [ ] Cache trending movies (1 hour TTL)
  - [ ] Cache movie details (24 hour TTL)
  - [ ] Cache search results (30 min TTL)
  - [ ] Cache recommendations (2 hour TTL)
- [ ] Test Redis connection and caching
- #FUTURE[ ] Cache popular movies and genres
- #FUTURE[ ] Add database query optimization
- #FUTURE[ ] Implement pagination for large datasets

## 📚 API Documentation

### DRF & Swagger Setup

- [x] Configure drf-yasg for API documentation
- [ ] Add proper API endpoint descriptions
- [ ] Create API usage examples
- [ ] Add authentication documentation
- [x] Test all API endpoints with Swagger UI

## 🧪 Testing & Quality

### Testing Implementation

- [ ] Set up Django test framework
- [ ] Write unit tests for models
- [ ] Create API endpoint tests
- [ ] Add authentication tests
- [ ] Test recommendation algorithms
- [ ] Create integration tests for Docker setup

### Code Quality

- [ ] Add code linting (flake8/black)
- [ ] Implement pre-commit hooks
- [x] Add type hints where appropriate
- [ ] Create proper error handling
- [ ] Add logging configuration

## 🚀 Deployment & DevOps

### CI/CD Pipeline

- [ ] Set up GitHub Actions workflow
- [ ] Add automated testing in CI
- [x] Configure Docker image building
- [ ] Add deployment automation
- [ ] Set up environment-specific configs

### Production Setup

- [ ] Configure production database settings
- [ ] Set up static file serving
- [ ] Add monitoring and logging
- [ ] Configure backup strategies
- [ ] Set up SSL/HTTPS

## 📱 Frontend Considerations (Future)

### API Preparation

- [ ] Ensure API is frontend-ready
- [ ] Add proper error responses
- [ ] Implement consistent data formats
- [ ] Add API versioning
- [ ] Create comprehensive API documentation

## 🔧 Technical Debt & Improvements

### Performance Optimization

- [ ] Add database indexing
- [ ] Implement query optimization
- [ ] Add response compression
- [ ] Monitor and optimize API response times

### Security Hardening

- [ ] Add request validation
- [ ] Implement rate limiting
- [ ] Add security headers
- [ ] Configure proper CORS policies
- [ ] Add audit logging

## 📝 Documentation

### Project Documentation

- [ ] Update README.md with setup instructions
- [ ] Create API usage guide
- [ ] Add database schema documentation
- [ ] Create deployment guide
- [ ] Add troubleshooting section

---

## 🎯 Current Priority Order (5 Days Sprint)

**HIGH PRIORITY (Must Complete):**

1. **Movie Endpoints Creation** - Core movie API endpoints

   - [x] Create movies app structure
   - [x] Trending movies endpoint (GET /api/movies/trending/)
   - [ ] Movie search endpoint (GET /api/movies/search/)
   - [x] Movie details endpoint (GET /api/movies/{id}/)
   - [ ] Movie recommendations endpoint (GET /api/movies/{id}/recommendations/)

2. **Basic Caching Implementation** - Redis caching for TMDB API calls
   - [ ] Set up Redis caching for TMDB API responses
   - [ ] Cache trending movies (1 hour TTL)
   - [ ] Cache movie details (24 hour TTL)
   - [ ] Cache search results (30 min TTL)

**MEDIUM PRIORITY (As much as Time Allows):** 3. **API Documentation** - Make Swagger docs more detailed for endpoints 4. **URL Configuration** - Ensure all endpoints are properly routed 5. **Error Handling** - Proper error responses for movie endpoints

**LOW PRIORITY (Future Sprint):** 6. **Testing** - Basic endpoint tests 7. **Advanced Features** - Filtering, pagination, etc.

---

**Last Updated:** August 4, 2025
**Project Status:** 🚀 SPRINT MODE - Movie Endpoints & Caching (5 Days)
