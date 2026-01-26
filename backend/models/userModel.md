# User Model

## Description
Represents a registered teacher in the system.

## Attributes
- userId (unique identifier)
- fullName
- email
- password
- institution
- experienceYears

## Constraints
- Email must be unique
- Required fields: fullName, email, password

## Usage
This model is used for:
- Authentication processes
- Teacher profile management
- Authorization checks
