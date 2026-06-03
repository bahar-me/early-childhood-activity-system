# System Architecture Diagram

## General Architecture

```text
Teacher / User
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

## AI Flow
Frontend Adaptation Request
      |
      v
Flask AI Route
      |
      v
AI Service
      |
      |-- Gemini API
      |
      |-- Ollama Local LLM
      |
      |-- Mock AI Fallback


## Report Flow
Selected Activities
      |
      v
Activity Report Component
      |
      v
HTML Print Layout
      |
      v
PDF / Print Output


