"""
Hospital Management System - Main Application
Main entry point for the Flask application
"""

import os
from flask import Flask, render_template, redirect, url_for
from config import get_config
from extensions import db, login_manager, bcrypt


def create_app(config_name=None):
    """
    Application factory pattern
    Creates and configures the Flask application

    Args:
        config_name (str): Configuration environment name

    Returns:
        Flask app instance
    """
    # Create Flask app instance
    app = Flask(__name__)

    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(get_config(config_name))

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Configure Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Import models (needed for database creation)
    with app.app_context():
        from models import user, admin, doctor, patient, specialization, appointment, treatment

        # Create database tables
        db.create_all()

        # Initialize database with default data
        from utils.database import init_db
        init_db(db, bcrypt)

    # Register blueprints (controllers)
    with app.app_context():
        from controllers.auth_controller import auth_bp
        from controllers.admin_controller import admin_bp
        from controllers.doctor_controller import doctor_bp
        from controllers.patient_controller import patient_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(doctor_bp, url_prefix='/doctor')
        app.register_blueprint(patient_bp, url_prefix='/patient')

        # Optional: Register API blueprints
        # from api.doctor_api import doctor_api_bp
        # app.register_blueprint(doctor_api_bp, url_prefix='/api/v1')

    # User loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        return User.query.get(int(user_id))

    # Home route
    @app.route('/')
    def index():
        """Landing page route with dynamic statistics"""
        from models.doctor import Doctor
        from models.patient import Patient
        from models.appointment import Appointment
        from models.specialization import Specialization

        # Get real statistics from database
        total_doctors = Doctor.query.count()
        total_patients = Patient.query.count()
        total_appointments = Appointment.query.count()
        total_specializations = Specialization.query.count()

        # Get all specializations for showcase
        specializations = Specialization.query.order_by(Specialization.name).limit(6).all()

        # Get featured doctors (top 4 by experience)
        # Filter by active users through the user relationship
        from models.user import User
        featured_doctors = Doctor.query.join(User, Doctor.user_id == User.id).filter(
            User.is_active == True
        ).order_by(Doctor.experience_years.desc()).limit(4).all()

        return render_template('index.html',
                             total_doctors=total_doctors,
                             total_patients=total_patients,
                             total_appointments=total_appointments,
                             total_specializations=total_specializations,
                             specializations=specializations,
                             featured_doctors=featured_doctors)

    # Error handlers
    @app.errorhandler(403)
    def forbidden(e):
        """Handle 403 Forbidden errors"""
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        """Handle 404 Not Found errors"""
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        """Handle 500 Internal Server errors"""
        return render_template('errors/500.html'), 500

    # Context processor for template variables
    @app.context_processor
    def inject_app_info():
        """Inject application info into all templates"""
        return {
            'app_name': app.config['APP_NAME'],
            'app_version': app.config['APP_VERSION']
        }

    return app


if __name__ == '__main__':
    """
    Run the application
    Only runs when executing this file directly
    """
    # Create app instance
    app = create_app()

    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))

    # Run the app
    print(f"\n{'='*60}")
    print(f"Hospital Management System Starting...")
    print(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"Running on: http://127.0.0.1:{port}/")
    print(f"{'='*60}\n")

    app.run(
        host='127.0.0.1',
        port=port,
        debug=app.config['DEBUG']
    )
