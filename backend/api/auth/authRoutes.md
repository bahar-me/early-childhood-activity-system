# Authentication API Routes

This document describes the authentication-related API endpoints of the system.

## Base Path
/api/auth

## POST /login

### Description
Authenticates a registered user using email and password credentials.  
The user can have one of the following roles: teacher, school_admin, or system_admin.

### Request Parameters
- email (string)
- password (string)

### Preconditions
- The teacher must be registered in the system.

### Success Response
- Authentication successful
- Access token and refresh token are generated
- User information and role are returned

### Error Responses
- Invalid credentials
- Missing required fields

### Related Service
- Authentication service
