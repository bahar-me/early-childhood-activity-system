# Project Report Summary

## Project Name

Early Childhood Activity Recommendation and Planning System

## Project Purpose

The purpose of this project is to support preschool teachers in planning, adapting, and reporting educational activities according to teacher profiles, class characteristics, age groups, available resources, and learning objectives.

## Main Features

* JWT-based authentication and authorization
* Role-based access control (Teacher, School Administrator, System Administrator)
* Teacher profile management
* Class profile management
* Activity library management
* Activity planning and reporting
* AI-supported activity adaptation
* PDF report generation and sharing
* School administrator dashboard
* Mobile application support with Capacitor
* Local AI support with Ollama
* Cloud AI integration with Gemini

## Technologies Used

### Frontend

* React
* TypeScript
* Vite
* Tailwind CSS

### Backend

* Flask
* SQLAlchemy
* Flask-Migrate
* Flask-JWT-Extended
* SQLite
* REST API Architecture

### Artificial Intelligence

* Gemini API
* Ollama Local LLM
* Mock AI Fallback System

### Mobile

* Capacitor
* Android Platform Support

### Testing

* Pytest
* Authentication Tests
* Authorization Tests
* School Management Tests
* API Integration Tests

## Security Features

* Password hashing
* JWT access and refresh tokens
* Role-based authorization
* Protected API endpoints
* Refresh token revocation
* Restricted registration endpoint
* Environment variable configuration
* Production configuration validation
* CORS restrictions

## Result

The project provides a functional prototype that enables preschool teachers to manage profiles, create activity plans, adapt activities with artificial intelligence support, generate reports, and access the system through both web and mobile platforms.

The system was successfully tested and validated through automated backend tests and real usage scenarios.
