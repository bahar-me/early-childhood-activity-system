# Login Service

## Purpose
Handles user authentication and token generation.

## Responsibilities
- Validate login input fields
- Authenticate user credentials
- Generate access token
- Generate refresh token
- Store refresh token in the database
- Return authenticated user information

## Input
- Email
- Password

## Validation Rules
- Email must not be empty
- Password must not be empty
- User must exist in the system
- Password must match the stored password hash

## Authentication Logic
- Find the user by email
- Compare the provided password with the stored password hash
- If credentials are valid, generate JWT access and refresh tokens
- Add user role and school_id to access token claims
- Store the refresh token as active in the database

## Output
- Success:
  - access_token
  - refresh_token
  - user information
- Failure:
  - appropriate error message

## Error Handling
- Validation error: missing email or password
- Authentication error: invalid credentials
- Token error: refresh token could not be created or stored