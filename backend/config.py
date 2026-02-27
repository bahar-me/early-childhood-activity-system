import os
from datetime import timedelta

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = ENVIRONMENT == "development"

# Security
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    if os.getenv("ENVIRONMENT") == "development":
        SECRET_KEY = "dev_secret_key_change_in_production"
    else:
        raise ValueError("SECRET_KEY environment variable is not set")

# JWT Configuration
JWT_ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRATION = timedelta(minutes=15)
REFRESH_TOKEN_EXPIRATION = timedelta(days=7)

# Database (if needed)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")