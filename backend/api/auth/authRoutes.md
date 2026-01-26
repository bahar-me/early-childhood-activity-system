# Authentication API Routes

This document describes the authentication-related API endpoints of the system.

## Base Path
/api/auth

## POST /login

### Description
Authenticates a teacher using email and password credentials.

### Request Parameters
- email (string)
- password (string)

### Preconditions
- The teacher must be registered in the system.

### Success Response
- Authentication successful
- User session or token is generated

### Error Responses
- Invalid credentials
- Missing required fields

### Related Service
- loginService
