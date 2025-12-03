"""
Authentication Controller
Handles login, logout, and patient registration
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from extensions import db, bcrypt
from models.user import User
from models.patient import Patient
from utils.decorators import anonymous_required
from utils.helpers import validate_email, validate_phone, sanitize_string
from datetime import datetime

# Create blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
@anonymous_required
def login():
    """
    Login route for all user types
    GET: Display login form
    POST: Process login credentials
    """
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)

        # Validate input
        if not username or not password:
            flash('Please enter both username and password.', 'danger')
            return render_template('login.html')

        # Find user
        user = User.query.filter_by(username=username).first()

        if not user:
            flash('Invalid username or password.', 'danger')
            return render_template('login.html')

        # Check if account is active
        if not user.is_active:
            flash('Your account has been deactivated. Please contact the administrator.', 'danger')
            return render_template('login.html')

        # Verify password
        if not bcrypt.check_password_hash(user.password_hash, password):
            flash('Invalid username or password.', 'danger')
            return render_template('login.html')

        # Login successful
        login_user(user, remember=remember)
        flash(f'Welcome back, {username}!', 'success')

        # Redirect based on role
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)

        if user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif user.role == 'doctor':
            return redirect(url_for('doctor.dashboard'))
        elif user.role == 'patient':
            return redirect(url_for('patient.dashboard'))
        else:
            return redirect(url_for('index'))

    # GET request - show login form
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """
    Logout route for all user types
    Clears session and redirects to login page
    """
    if current_user.is_authenticated:
        username = current_user.username
        logout_user()
        flash(f'Goodbye, {username}! You have been logged out successfully.', 'info')

    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
@anonymous_required
def register():
    """
    Patient registration route
    GET: Display registration form
    POST: Process registration
    """
    if request.method == 'POST':
        # Get form data
        username = sanitize_string(request.form.get('username', ''), max_length=80)
        email = sanitize_string(request.form.get('email', ''), max_length=120)
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        name = sanitize_string(request.form.get('name', ''), max_length=100)
        contact_number = sanitize_string(request.form.get('contact_number', ''), max_length=15)
        date_of_birth = request.form.get('date_of_birth', '')
        gender = request.form.get('gender', '')
        address = sanitize_string(request.form.get('address', ''))
        blood_group = request.form.get('blood_group', '')
        emergency_contact = sanitize_string(request.form.get('emergency_contact', ''), max_length=15)

        # Validation
        errors = []

        # Required fields
        if not username:
            errors.append('Username is required.')
        if not email:
            errors.append('Email is required.')
        if not password:
            errors.append('Password is required.')
        if not name:
            errors.append('Full name is required.')
        if not contact_number:
            errors.append('Contact number is required.')

        # Username length
        if len(username) < 3:
            errors.append('Username must be at least 3 characters long.')

        # Email validation
        if email and not validate_email(email):
            errors.append('Please enter a valid email address.')

        # Password validation
        if len(password) < 6:
            errors.append('Password must be at least 6 characters long.')

        if password != confirm_password:
            errors.append('Passwords do not match.')

        # Phone validation
        if contact_number and not validate_phone(contact_number):
            errors.append('Please enter a valid 10-digit phone number.')

        # Check if username already exists
        if User.query.filter_by(username=username).first():
            errors.append('Username already exists. Please choose another.')

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered. Please use another or login.')

        # Gender validation
        if gender and gender not in ['Male', 'Female', 'Other']:
            errors.append('Please select a valid gender.')

        # Blood group validation
        if blood_group and not Patient.validate_blood_group(blood_group):
            errors.append('Please enter a valid blood group.')

        # If there are errors, show them and return to form
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('register.html', form_data=request.form)

        # Create user and patient
        try:
            # Hash password
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

            # Create user
            user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                role='patient'
            )
            db.session.add(user)
            db.session.flush()  # Get user.id

            # Parse date of birth
            dob = None
            if date_of_birth:
                try:
                    dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
                except:
                    pass

            # Create patient profile
            patient = Patient(
                user_id=user.id,
                name=name,
                contact_number=contact_number,
                date_of_birth=dob,
                gender=gender if gender else None,
                address=address if address else None,
                blood_group=blood_group if blood_group else None,
                emergency_contact=emergency_contact if emergency_contact else None
            )
            db.session.add(patient)
            db.session.commit()

            flash(f'Registration successful! Welcome, {name}. Please login to continue.', 'success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}. Please try again.', 'danger')
            return render_template('register.html', form_data=request.form)

    # GET request - show registration form
    return render_template('register.html')


@auth_bp.route('/forgot-password')
def forgot_password():
    """
    Forgot password route (placeholder for future implementation)
    """
    flash('Password reset feature is not yet implemented. Please contact the administrator.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/change-password', methods=['GET', 'POST'])
def change_password():
    """
    Change password route for logged-in users
    """
    if not current_user.is_authenticated:
        flash('Please login to change your password.', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validation
        if not current_password or not new_password or not confirm_password:
            flash('All fields are required.', 'danger')
            return render_template('change_password.html')

        # Verify current password
        if not bcrypt.check_password_hash(current_user.password_hash, current_password):
            flash('Current password is incorrect.', 'danger')
            return render_template('change_password.html')

        # Validate new password
        if len(new_password) < 6:
            flash('New password must be at least 6 characters long.', 'danger')
            return render_template('change_password.html')

        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
            return render_template('change_password.html')

        # Update password
        try:
            current_user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
            db.session.commit()
            flash('Password changed successfully!', 'success')

            # Redirect based on role
            if current_user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif current_user.role == 'doctor':
                return redirect(url_for('doctor.dashboard'))
            elif current_user.role == 'patient':
                return redirect(url_for('patient.dashboard'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error changing password: {str(e)}', 'danger')

    # GET request - show change password form
    return render_template('change_password.html')


# ==================== LEGAL & HELP PAGES ====================

@auth_bp.route('/privacy-policy')
def privacy_policy():
    """
    Privacy Policy page
    Public access - explains data collection and usage
    """
    return render_template('privacy_policy.html')


@auth_bp.route('/terms-of-service')
def terms_of_service():
    """
    Terms of Service page
    Public access - user agreement and policies
    """
    return render_template('terms_of_service.html')


@auth_bp.route('/faq')
def faq():
    """
    Frequently Asked Questions page
    Public access - help and common questions
    """
    return render_template('faq.html')
