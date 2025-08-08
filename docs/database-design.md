# MovieRec - Database Design & ERD

## Database Architecture Overview

The MovieRec system uses PostgreSQL as the primary database with Redis for caching. The database design follows Django's ORM patterns and maintains referential integrity while supporting the application's core functionality.

## Entity Relationship Diagram

```
┌─────────────────────────────────┐
│            User                 │
├─────────────────────────────────┤
│ PK  id (UUID)                  │
│     username (CharField)        │
│     email (EmailField)          │
│     password (CharField)        │
│     first_name (CharField)      │
│     last_name (CharField)       │
│     last_login (DateTimeField)  │
│     date_joined (DateTimeField) │
│     is_active (BooleanField)    │
│     is_staff (BooleanField)     │
│     is_superuser (BooleanField) │
└─────────────────────────────────┘
                │
                │ 1:N
                ▼
┌─────────────────────────────────┐
│          Favorites              │
├─────────────────────────────────┤
│ PK  id (UUID)                  │
│ FK  user_id → User.id          │
│     tmdb_id (IntegerField)      │
│     item_name (CharField)       │
│     poster_url (CharField)      │
│     created_at (DateTimeField)  │
│                                 │
│ UNIQUE(tmdb_id)                │
└─────────────────────────────────┘
```

## Entity Specifications

### User Entity (Custom User Model)

**Purpose**: Extends Django's AbstractUser to handle authentication and user management.

**Attributes**:

- `id` (UUID, Primary Key): Unique identifier using UUID for better security
- `username` (CharField): Unique username for login
- `email` (EmailField): User's email address
- `password` (CharField): Hashed password using Django's authentication
- `first_name` (CharField): User's first name (optional)
- `last_name` (CharField): User's last name (optional)
- `last_login` (DateTimeField): Timestamp of last login
- `date_joined` (DateTimeField): Account creation timestamp
- `is_active` (BooleanField): Account active status
- `is_staff` (BooleanField): Staff privileges flag
- `is_superuser` (BooleanField): Superuser privileges flag

**Relationships**:

- One-to-Many with Favorites (one user can have multiple favorites)

**Constraints**:

- `username` must be unique
- `email` is unique (enforced at database level)

### Favorites Entity

**Purpose**: Stores user's favorite movies and TV series with metadata from TMDB.

**Attributes**:

- `id` (UUID, Primary Key): Unique identifier for each favorite
- `user_id` (UUID, Foreign Key): References User.id
- `tmdb_id` (Integer): The Movie Database ID for the content
- `item_name` (CharField): Movie/TV series title (fetched from TMDB)
- `poster_url` (CharField): Poster image URL (stored as text with default "null")
- `created_at` (DateTimeField): Timestamp when favorite was added

**Relationships**:

- Many-to-One with User (multiple favorites belong to one user)

**Constraints**:

- `tmdb_id` has unique constraint (prevents duplicate TMDB items globally)
- `user_id` is required (NOT NULL, foreign key)
- `tmdb_id` is required
- `item_name` has default value "null"
- `poster_url` has default value "null"

## Design Decisions & Rationale

### 1. Custom User Model

**Decision**: Extend AbstractUser instead of using Django's default User model.

**Rationale**:

- Provides flexibility for future user profile extensions
- Uses UUID primary keys for better security and scalability
- Follows Django best practices for custom authentication

### 2. UUID Primary Keys

**Decision**: Use UUIDs instead of auto-incrementing integers.

**Rationale**:

- Enhanced security (non-guessable IDs)
- Better for distributed systems and API exposure
- Eliminates enumeration attacks on user accounts

### 3. Denormalized Movie Data

**Decision**: Store movie name and poster URL directly in Favorites table.

**Rationale**:

- Reduces API calls to TMDB for favorites listing
- Improves performance for user's favorites page
- Provides offline capability for basic favorite information
- Trade-off: Some data duplication for better performance

### 4. Global Unique Constraint on TMDB ID

**Decision**: Prevent duplicate TMDB items globally using unique constraint on tmdb_id.

**Rationale**:

- Ensures data integrity at database level
- Prevents duplicate movies/TV shows across all users
- Simpler constraint implementation

### 5. No Local Movie Storage

**Decision**: Don't store complete movie data locally, only reference TMDB IDs.

**Rationale**:

- Reduces database size and complexity
- Always gets fresh movie data from TMDB
- Avoids data synchronization issues
- Complies with TMDB terms of service

## Database Indexes

### Automatic Indexes (Django ORM)

- Primary key indexes on all `id` fields
- Unique constraint index on `User.username`
- Foreign key index on `Favorites.user_id`

### Recommended Additional Indexes

```sql
-- For efficient favorites lookup by user
CREATE INDEX idx_favorites_user_created
ON accounts_favorites(user_id, created_at DESC);

-- For TMDB ID lookups (checking duplicates)
CREATE INDEX idx_favorites_tmdb_id
ON accounts_favorites(tmdb_id);

-- For user authentication queries
CREATE INDEX idx_user_email
ON accounts_user(email);
```

## Data Integrity Rules

### Referential Integrity

- `Favorites.user_id` must reference valid `User.id`
- Cascade delete: When user is deleted, all their favorites are deleted

### Business Rules

- User cannot have duplicate TMDB items globally (unique constraint on tmdb_id)
- TMDB ID must be positive integer
- Item name has default value "null" and is populated from TMDB API
- Poster URL has default value "null" and is populated when available

### Data Validation

- Email format validation (Django EmailField)
- Username uniqueness (database constraint)
- Password strength (Django validators)
- Basic CharField length limits

## Caching Strategy

### Redis Configuration

Redis is configured as the default caching backend in Django settings with caching implemented on most API endpoints using Django's `cache_page` decorator.



### Cache Structure

Django's `cache_page` generates keys in the format: `views.decorators.cache.cache_page.{key_prefix}.{url_hash}.{language}.{timezone}`

**Implemented Cache Keys:**
```
- `views.decorators.cache.cache_page.trending_movies.{hash}` → Trending Movies (24h TTL)
- `views.decorators.cache.cache_page.trending_tv.{hash}` → Trending TV (24h TTL)
- `views.decorators.cache.cache_page.search_movies.{hash}` → Movie search (1h TTL)
- `views.decorators.cache.cache_page.search_tv.{hash}` → TV search (1h TTL)
- `views.decorators.cache.cache_page.details_movie.{hash}` → Movie details (2d TTL)
- `views.decorators.cache.cache_page.detail_tb.{hash}` → TV details (2d TTL)
- `views.decorators.cache.cache_page.recommendations_movies.{hash}` → Movie recommendations (2h TTL)
- `views.decorators.cache.cache_page.recommendations_tv.{hash}` → TV recommendations (2h TTL)
```

### TTL Strategy (Implemented)
- **Trending content**: 24 hours (daily updates for both movies and TV)
- **Movie/TV details**: 2 days (metadata rarely changes)  
- **Search results**: 1 hour (reasonable freshness)
- **Recommendations**: 2 hours (balance between freshness and performance)

## Security Considerations

### Data Protection

- Passwords hashed using Django's in-built hashing
- UUIDs prevent user enumeration attacks
- Foreign key constraints prevent orphaned data

### API Security

- JWT tokens for stateless authentication
- Environment variables for sensitive configuration

## Scalability Considerations

### Horizontal Scaling

- UUID primary keys support distributed databases
- Stateless authentication via JWT
- Redis caching can be clustered

### Vertical Scaling

- Efficient indexes for query performance
- Denormalized favorite data reduces joins
- Caching reduces database load

---

**Document Version**: 1.0  
**Last Updated**: August 8, 2025  
**Database Version**: PostgreSQL 17  
**Cache Version**: Redis 8.0
