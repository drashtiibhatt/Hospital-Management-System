"""
Flask Extensions
Centralized location for all Flask extension instances
This avoids circular imports when using the application factory pattern
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Initialize Flask extensions
# These will be initialized with the app in app.py using init_app()
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
