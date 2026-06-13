# General Guidelines

* Follow Flask + Service Layer architecture.
* Keep route files thin; business logic must stay in service files.
* Use SQLAlchemy ORM for all database operations.
* Avoid duplicated code and refactor repeated logic into helper functions.
* Keep functions focused on a single responsibility.
* Use type hints whenever possible.
* Write clean and readable code.
* Prefer Turkish error messages returned to the frontend.
* Use English for code, class names, function names, and comments.
* Use JWT authentication for protected endpoints.
* Use role-based authorization for all sensitive operations.
* Do not store passwords in plain text.
* Store secrets and API keys only in environment variables.

# Backend Guidelines

## API Routes

* Routes should only handle requests and responses.
* Validation and business logic must be placed in service files.
* Return consistent JSON responses.
* Use proper HTTP status codes.

## Database

* Use SQLAlchemy models.
* Use Alembic migrations for schema changes.
* Prefer relationships over manual joins when appropriate.
* Avoid unnecessary database queries.

## Security

* Use JWT authentication.
* Protect sensitive endpoints with role checks.
* System Admin has full access.
* School Admin can only manage data belonging to their own school.
* Teachers can only access teacher-level functionality.
* Validate all incoming user data.
* Never expose sensitive information in API responses.

# Frontend Guidelines

* Use React functional components.
* Use TypeScript for all new code.
* Keep components small and reusable.
* Extract repeated UI into reusable components.
* Use async/await for API requests.
* Handle loading and error states properly.
* Display user-friendly Turkish messages.

# AI Integration Guidelines

* Primary AI provider: Gemini API.
* Secondary AI provider: Ollama Local LLM.
* Fallback provider: Mock AI service.
* Always validate AI responses before using them.
* Expect structured JSON responses.
* Handle malformed responses gracefully.

# Testing Guidelines

* Add or update tests when changing backend behavior.
* Run pytest before committing changes.
* Maintain passing authentication and authorization tests.
* Keep test coverage focused on business-critical features.

# Project Context

Project Name: Early Childhood Activity Recommendation and Planning System

Main Features:

* Authentication and authorization
* Teacher profiles
* Class profiles
* Activity management
* Activity planning
* AI-supported activity adaptation
* PDF report generation
* School administrator dashboard
* Android support with Capacitor

Technology Stack:

* React
* TypeScript
* Flask
* SQLAlchemy
* JWT
* SQLite
* Gemini API
* Ollama
* Capacitor
