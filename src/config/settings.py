"""
Settings and Configuration Management
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict


class Settings(BaseSettings):
    """Application settings"""
    
    model_config = ConfigDict(
        case_sensitive=True,
        extra="ignore"  # Ignore extra environment variables not defined in Settings
    )
    
    # Project
    PROJECT_NAME: str = "Real Estate CRM API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    
    # Server
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    
    # Database
    DATABASE_URL: str = Field(default="postgresql+asyncpg://postgres:realestatecrm@localhost:5432/realestate_db", env="DATABASE_URL")
    DATABASE_ECHO: bool = Field(default=False, env="DATABASE_ECHO")
    DATABASE_POOL_SIZE: int = Field(default=10, env="DATABASE_POOL_SIZE")
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    REDIS_CACHE_TTL: int = Field(default=3600, env="REDIS_CACHE_TTL")
    
    # JWT
    SECRET_KEY: str = Field(default="your-secret-key-change-in-production", env="SECRET_KEY")
    JWT_SECRET_KEY: str = Field(default="your-jwt-secret-key-change-in-production", env="JWT_SECRET_KEY")
    ALGORITHM: str = "HS256"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_EXPIRATION_HOURS: int = 1
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    JWT_REFRESH_EXPIRATION_DAYS: int = 7
    
    # Google OAuth
    GOOGLE_CLIENT_ID: str = Field(default="", env="GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = Field(default="", env="GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI: str = Field(default="http://localhost:8000/api/auth/google/callback", env="GOOGLE_REDIRECT_URI")
    
    # Email Configuration
    SMTP_HOST: str = Field(default="smtp.gmail.com", env="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USER: str = Field(default="", env="SMTP_USER")
    SMTP_PASSWORD: str = Field(default="", env="SMTP_PASSWORD")
    SMTP_FROM_EMAIL: str = Field(default="noreply@realestate.com", env="SMTP_FROM_EMAIL")
    
    # Admin Configuration
    ADMIN_EMAIL_DOMAIN: str = Field(default="admin.realestate.com", env="ADMIN_EMAIL_DOMAIN")
    
    # CORS
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000", "http://localhost:8000"])
    
    # Features
    ENABLE_JOBS: bool = Field(default=True, env="ENABLE_JOBS")
    ENABLE_NOTIFICATIONS: bool = Field(default=True, env="ENABLE_NOTIFICATIONS")
    ENABLE_PAYMENTS: bool = Field(default=True, env="ENABLE_PAYMENTS")


settings = Settings()
