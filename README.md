# AI-Supported Early Childhood Activity Management and Recommendation System

## Project Overview

This project was developed as a graduation project to support teachers in early childhood education.

The system helps teachers manage classroom information, plan activities, generate reports, and adapt activities using Artificial Intelligence (AI).

The application follows a modular architecture and provides both web and mobile-ready support.

---

## Main Features

### User Management

* JWT-based authentication
* Role-based authorization
* System Admin, School Admin, and Teacher roles

### School Management

* Create, update, list, and delete schools
* Access control based on user roles

### Teacher and Class Profiles

* Teacher profile management
* Class profile management
* Learning focus and resource tracking

### Activity Planning

* Activity listing and management
* Profile-based activity planning workflow

### AI-Supported Activity Adaptation

* Activity adaptation based on teacher prompts
* Gemini API integration
* Ollama local LLM integration
* Automatic fallback mechanism
* AI-generated activity drafts

AI Flow:

```text
Gemini API
↓
Ollama Local LLM
↓
Mock AI
```

### Reporting

* Activity report generation
* Print-friendly layout
* PDF export support

### Mobile Support

* Capacitor integration
* Android project preparation

---

## System Architecture

```text
Teacher/User
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
Database
```

---

## Technologies Used

### Frontend

* React
* TypeScript
* Vite
* Tailwind CSS

### Backend

* Flask
* SQLAlchemy
* JWT Authentication
* Alembic

### Artificial Intelligence

* Google Gemini API
* Ollama Local LLM
* Llama 3.2
* Multi-provider AI fallback architecture

### Testing

* Pytest
* Authentication testing
* Authorization testing
* API Endpoint testing

### Mobile

* Capacitor
* Android

---

## Installation

### Backend

* Flask
* Flask-SQLAlchemy
* Flask-JWT-Extended
* Flask-Migrate (Alembic)
* REST API Architecture

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Ollama

```bash
ollama run llama3.2
```

---

## Environment Variables

Example:

```env
SECRET_KEY=
JWT_SECRET_KEY=

GEMINI_API_KEY=

OLLAMA_ENABLED=true
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

---

## Running Tests

```bash
pytest
```

---

## Project Status

### Completed

* Authentication
* Authorization
* School Management
* Teacher and Class Profiles
* Activity Planning
* AI Integration
* PDF Reporting
* Backend Testing

### In Progress

* Final documentation review
* Android deployment validation

### Planned

* Final presentation preparation

---

## License

This project was developed for academic purposes.

## Academic Context

This project was developed as a Computer Engineering graduation project and demonstrates the integration of web technologies, artificial intelligence services, database management, authentication mechanisms, reporting systems, and mobile deployment preparation within a single educational platform.
