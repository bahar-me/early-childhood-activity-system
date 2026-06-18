# AI-Supported Early Childhood Activity Management and Recommendation System

## Project Overview

This project was developed as a Computer Engineering graduation project to support teachers working in early childhood education.

The system enables teachers to manage classroom information, create and adapt educational activities, generate reports, and receive AI-assisted recommendations based on classroom and teacher profiles.

The application follows a modular full-stack architecture and supports both web deployment and mobile integration.

---

## Live Deployment

### Frontend

Deployed on **Vercel**

### Backend

Deployed on **Render**

### Database

**PostgreSQL** hosted on Render

---

## Main Features

### User Management

* JWT-based authentication
* Role-based authorization (RBAC)
* System Admin, School Admin, and Teacher roles
* Secure access control

### School Management

* Create, update, list, and delete schools
* Role-based access restrictions
* School-specific data management

### Teacher and Class Profiles

* Teacher profile management
* Class profile management
* Learning focus tracking
* Resource preference management

### Activity Management

* Activity listing and filtering
* Favorite activities
* Activity selection workflow
* Activity plan generation

### AI-Supported Activity Adaptation

* Teacher prompt-based activity adaptation
* Google Gemini API integration
* Ollama Local LLM integration
* Automatic fallback architecture
* AI-generated activity recommendations

AI Flow:

```text
Gemini API
      ↓
Ollama Local LLM
      ↓
Mock AI
```

### Reporting

* Activity plan report generation
* Print-friendly report layout
* PDF export support
* Teacher and class profile integration

### Mobile Support

* Capacitor integration
* Android project preparation
* Mobile-ready architecture

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
PostgreSQL Database
```

---

## Technologies Used

### Frontend

* React
* TypeScript
* Vite
* Tailwind CSS
* Capacitor

### Backend

* Flask
* SQLAlchemy
* Flask-JWT-Extended
* Flask-Migrate (Alembic)
* REST API Architecture

### Database

* PostgreSQL
* SQLAlchemy ORM

### Artificial Intelligence

* Google Gemini API
* Ollama Local LLM
* Llama 3.2
* Multi-provider fallback architecture

### Testing

* Pytest
* Authentication testing
* Authorization testing
* API endpoint testing

### Deployment

* Vercel (Frontend)
* Render (Backend)
* Render PostgreSQL

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

DATABASE_URL=

GEMINI_API_KEY=

OLLAMA_ENABLED=true
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

VITE_API_BASE_URL=http://localhost:5000
```

---

## Running Tests

```bash
pytest
```

---

## Project Status

### Completed

* Authentication and Authorization
* School Management
* Teacher and Class Profiles
* Activity Management
* AI Integration
* PostgreSQL Integration
* PDF Reporting
* Backend Testing
* Render Deployment
* Vercel Deployment

### Future Improvements

* Advanced AI recommendations
* Enhanced mobile experience
* Additional reporting options

---

## License

This project was developed for academic purposes.

---

## Academic Context

This project was developed as a Computer Engineering graduation project and demonstrates the integration of:

* Full-stack web development
* REST API architecture
* Authentication and authorization systems
* Artificial intelligence services
* Database management
* Reporting systems
* Cloud deployment
* Mobile application preparation

within a single educational technology platform.
