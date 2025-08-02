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
- #FIXME [ ] Roll back migration to  the beginning to alter AUTH_USER_MODEL
- [x] Design movie database schema (ERD)
- [ ] Create User profile model (preferences, ratings history)
- [x] Run initial migrations
- [ ] Create database seed data/fixtures

## 🔐 Authentication & Authorization

### User Management (accounts app)
- [ ] Implement user registration endpoint
- [ ] Implement JWT login/logout endpoints
- [ ] Add password reset functionality
- [ ] Create user profile management
- [ ] Add email verification (optional)
- [ ] Implement role-based permissions (user/admin)

### Security
- [ ] Configure CORS headers properly
- [ ] Add rate limiting to API endpoints
- [ ] Implement input validation and sanitization
- [ ] Add API authentication middleware

## 🎬 Core Movie Features

### Movie Management (movies app)
- [ ] Create movie CRUD endpoints
- [ ] Implement movie search and filtering
- [ ] Add genre-based filtering
- [ ] Create movie recommendation algorithm
- [ ] Add movie rating system
- [ ] Implement user watchlist functionality
- [ ] Add movie reviews and comments

### Movie Data
- [ ] Integrate with external movie API (TMDB)
    - [x] trending weekly movies and series
    - [x] movie  and series search
        - [x] query parameter support
    - [x] specific movie
    - [x] request error handling
    - [ ]item id input validation ( API level?)
    -#FUTURE: [ ] recommendation filtering
-#FUTURE: [ ] Add movie poster/image handling?


### Caching & Performance
- [ ] Implement Redis caching for 3rd party API calls
- [ ] Cache popular movies and genres
- [ ] Add database query optimization
- [ ] Implement pagination for large datasets

## 📚 API Documentation

### DRF & Swagger Setup
- [ ] Configure drf-yasg for API documentation
- [ ] Add proper API endpoint descriptions
- [ ] Create API usage examples
- [ ] Add authentication documentation
- [ ] Test all API endpoints with Swagger UI



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
- [ ] Add type hints where appropriate
- [ ] Create proper error handling
- [ ] Add logging configuration

## 🚀 Deployment & DevOps

### CI/CD Pipeline
- [ ] Set up GitHub Actions workflow
- [ ] Add automated testing in CI
- [ ] Configure Docker image building
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
- [ ] Configure static file caching
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

## 🎯 Current Priority Order

1. **External API Integration** - TMDB API integration and data fetching
2. **API Endpoints Creation** - RESTful endpoints for movie data
3. **Core Models** - Movie, User, Rating models with API data structure
4. **Authentication** - JWT login/register
5. **Caching & Performance** - Redis caching for external API calls
6. **API Documentation** - Swagger setup for all endpoints
7. **Testing** - External API and endpoint tests
8. **Deployment** - Production ready setup

---

**Last Updated:** July 29, 2025
**Project Status:** API Integration & Endpoint Creation Phase
