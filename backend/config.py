import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt_secret_key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)  # 15 dakika
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)    # 7 gün

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_SECRET_KEY = "test_jwt_secret_key_for_pytest_2026_project_very_long"

class ProductionConfig(Config):
    DEBUG = False

    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    if not SECRET_KEY:
        raise RuntimeError("Production ortamında SECRET_KEY zorunludur")

    if not JWT_SECRET_KEY:
        raise RuntimeError("Production ortamında JWT_SECRET_KEY zorunludur")

config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}