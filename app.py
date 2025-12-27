"""
Hospital Management System - Main Application
Main entry point for the Flask application
"""

import os
from flask import Flask, render_template
from config import get_config
from extensions import db, login_manager, bcrypt


def create_app(config_name=None):
    """
    Application factory pattern
    Creates and configures the Flask application
    """
    app = Flask(__name__)

    # Load configuration
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")
    app.config.from_object(get_config(config_name))

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Configure Flask-Login
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"

    # Import models once inside app context (ensures SQLAlchemy registers them)
    with app.app_context():
        from models import (  # noqa: F401
            user,
            admin,
            doctor,
            patient,
            specialization,
            appointment,
            treatment,
        )

        # Optional: create/seed DB only if explicitly enabled
        # On Render, set INIT_DB=true once if you want to initialize tables
        if os.environ.get("INIT_DB", "").lower() == "true":
            db.create_all()
            from utils.database import init_db
            init_db(db, bcrypt)

    # Register blueprints
    from controllers.auth_controller import auth_bp
    from controllers.admin_controller import admin_bp
    from controllers.doctor_controller import doctor_bp
    from controllers.patient_controller import patient_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(doctor_bp, url_prefix="/doctor")
    app.register_blueprint(patient_bp, url_prefix="/patient")

    # User loader callback
    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        return User.query.get(int(user_id))

    # Home route
    @app.route("/")
    def index():
        from models.doctor import Doctor
        from models.patient import Patient
        from models.appointment import Appointment
        from models.specialization import Specialization
        from models.user import User

        total_doctors = Doctor.query.count()
        total_patients = Patient.query.count()
        total_appointments = Appointment.query.count()
        total_specializations = Specialization.query.count()

        specializations = (
            Specialization.query.order_by(Specialization.name).limit(6).all()
        )

        featured_doctors = (
            Doctor.query.join(User, Doctor.user_id == User.id)
            .filter(User.is_active.is_(True))
            .order_by(Doctor.experience_years.desc())
            .limit(4)
            .all()
        )

        return render_template(
            "index.html",
            total_doctors=total_doctors,
            total_patients=total_patients,
            total_appointments=total_appointments,
            total_specializations=total_specializations,
            specializations=specializations,
            featured_doctors=featured_doctors,
        )

    # Error handlers
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("errors/500.html"), 500

    # Context processor
    @app.context_processor
    def inject_app_info():
        return {
            "app_name": app.config.get("APP_NAME", "Hospital Management System"),
            "app_version": app.config.get("APP_VERSION", "1.0.0"),
        }

    return app


# Render (and Gunicorn) will import this
app = create_app(os.environ.get("FLASK_ENV", "production"))


# Local dev only
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config.get("DEBUG", False))
