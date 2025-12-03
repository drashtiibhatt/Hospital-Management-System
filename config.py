"""
Configuration settings for Hospital Management System
"""

import os
from datetime import timedelta

# Base directory of the application
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration class with common settings"""

    # Secret key for session management and CSRF protection
    # In production, this should be set via environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-please-change-in-production'

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'hospital.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # WTForms configuration
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # No time limit for CSRF tokens

    # Pagination
    ITEMS_PER_PAGE = 10

    # File upload configuration (for profile images - optional)
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Application settings
    APP_NAME = 'Hospital Management System'
    APP_VERSION = '1.0.0'

    # Email configuration (optional - for future use)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


class DevelopmentConfig(Config):
    """Development environment configuration"""

    DEBUG = True
    TESTING = False

    # More verbose error messages in development
    EXPLAIN_TEMPLATE_LOADING = False

    # Disable some security features for easier development
    WTF_CSRF_ENABLED = True  # Keep CSRF enabled even in dev


class ProductionConfig(Config):
    """Production environment configuration"""

    DEBUG = False
    TESTING = False

    # In production, SECRET_KEY must be set via environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY') or Config.SECRET_KEY

    # Enhanced security for production
    SESSION_COOKIE_SECURE = True  # Requires HTTPS
    WTF_CSRF_ENABLED = True

    # Use a production-grade database (PostgreSQL/MySQL)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    def __init__(self):
        """Validate production configuration"""
        super().__init__()
        if not os.environ.get('SECRET_KEY'):
            raise ValueError("SECRET_KEY environment variable must be set in production!")


class TestingConfig(Config):
    """Testing environment configuration"""

    TESTING = True
    DEBUG = True

    # Use in-memory SQLite database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False

    # Faster password hashing for tests
    BCRYPT_LOG_ROUNDS = 4


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """
    Get configuration based on environment

    Args:
        env (str): Environment name (development/production/testing)

    Returns:
        Config class
    """
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')

    return config.get(env, config['default'])
