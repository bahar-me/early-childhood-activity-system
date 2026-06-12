# User Model

## Description
Represents a registered user in the system.  
A user can have one of the following roles: teacher, school_admin, or system_admin.

## Attributes
- id: unique identifier
- email: user email address
- password_hash: hashed password
- role: user role in the system
- school_id: related school identifier, nullable for system_admin
- created_at: creation date

## Constraints
- Email must be unique
- Required fields: email, password_hash, role
- school_id can be null for system-level users

## Usage
This model is used for:
- Authentication processes
- Role-based authorization checks
- Linking teachers and school administrators to schools
- Refresh token ownership