# AI-Supported Early Childhood Activity Management System

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

* Gemini API integration
* Ollama Local LLM integration
* Automatic fallback mechanism

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
* Ollama
* Llama 3.2

### Testing

* Pytest

### Mobile

* Capacitor
* Android

---

## Installation

### Backend

```bash
pip install -r requirements.txt
py -m backend.app
```

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

* Final code cleanup
* Mobile testing

### Planned

* Android deployment validation
* Final presentation preparation

---

## License

This project was developed for academic purposes.
