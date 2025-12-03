"""
Controllers package
Contains all route handlers and business logic for the application
"""

# Import blueprints to make them available
from controllers.auth_controller import auth_bp
from controllers.admin_controller import admin_bp
from controllers.doctor_controller import doctor_bp
from controllers.patient_controller import patient_bp

__all__ = [
    'auth_bp',
    'admin_bp',
    'doctor_bp',
    'patient_bp'
]
