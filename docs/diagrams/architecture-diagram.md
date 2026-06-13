# System Architecture Diagram

## General Architecture

```text
Teacher / School Admin / System Admin
                |
                v
     React + TypeScript Frontend
                |
                v
          Flask REST API
                |
                v
           Service Layer
                |
                v
         SQLAlchemy ORM
                |
                v
             SQLite
```

## Authentication Flow

```text
User Login
     |
     v
Auth API
     |
     v
Authentication Service
     |
     v
JWT Access Token
JWT Refresh Token
     |
     v
Protected API Endpoints
```

## AI Adaptation Flow

```text
Frontend Adaptation Request
            |
            v
       Flask AI Route
            |
            v
        AI Service
            |
            +--> Gemini API
            |
            +--> Ollama Local LLM
            |
            +--> Mock AI Fallback
```

## Activity Planning Flow

```text
Teacher Profile
       |
       v
Class Profile
       |
       v
Activity Selection
       |
       v
Activity Plan Creation
       |
       v
Database Storage
```

## Reporting Flow

```text
Selected Activities
        |
        v
Activity Report Component
        |
        v
HTML Print Layout
        |
        v
PDF Generation
        |
        v
Share / Download
```

## School Administrator Flow

```text
School Administrator
          |
          v
School Overview API
          |
          v
Teacher Profiles
Class Profiles
Activity Plans
          |
          v
Statistics Dashboard
```
