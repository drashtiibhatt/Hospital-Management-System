"""
Custom Decorators
Role-based access control and other utility decorators
"""

from functools import wraps
from flask import abort, flash, redirect, url_for, request
from flask_login import current_user


def login_required_with_message(f):
    """
    Custom login required decorator with flash message
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    Decorator to restrict access to admin users only
    Usage: @admin_required
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))

        # Check if user is active
        if not current_user.is_active:
            flash('Your account has been deactivated. Please contact support.', 'danger')
            return redirect(url_for('auth.login'))

        # Check if user is admin
        if current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            abort(403)

        return f(*args, **kwargs)
    return decorated_function


def doctor_required(f):
    """
    Decorator to restrict access to doctor users only
    Usage: @doctor_required
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))

        # Check if user is active
        if not current_user.is_active:
            flash('Your account has been deactivated. Please contact support.', 'danger')
            return redirect(url_for('auth.login'))

        # Check if user is doctor
        if current_user.role != 'doctor':
            flash('You do not have permission to access this page.', 'danger')
            abort(403)

        return f(*args, **kwargs)
    return decorated_function


def patient_required(f):
    """
    Decorator to restrict access to patient users only
    Usage: @patient_required
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))

        # Check if user is active
        if not current_user.is_active:
            flash('Your account has been deactivated. Please contact support.', 'danger')
            return redirect(url_for('auth.login'))

        # Check if user is patient
        if current_user.role != 'patient':
            flash('You do not have permission to access this page.', 'danger')
            abort(403)

        return f(*args, **kwargs)
    return decorated_function


def role_required(*roles):
    """
    Decorator to restrict access to specific roles
    Usage: @role_required('admin', 'doctor')

    Args:
        *roles: Variable number of role names (admin, doctor, patient)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user is authenticated
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login', next=request.url))

            # Check if user is active
            if not current_user.is_active:
                flash('Your account has been deactivated. Please contact support.', 'danger')
                return redirect(url_for('auth.login'))

            # Check if user has required role
            if current_user.role not in roles:
                flash('You do not have permission to access this page.', 'danger')
                abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def check_account_active(f):
    """
    Decorator to check if user account is active
    Can be used with any role
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and not current_user.is_active:
            flash('Your account has been deactivated. Please contact support.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def anonymous_required(f):
    """
    Decorator to restrict access to anonymous users only
    (for pages like login, register that should not be accessible when logged in)
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            # Redirect to appropriate dashboard based on role
            if current_user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif current_user.role == 'doctor':
                return redirect(url_for('doctor.dashboard'))
            elif current_user.role == 'patient':
                return redirect(url_for('patient.dashboard'))
            else:
                return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


def validate_ownership(model, id_param='id', owner_field='user_id'):
    """
    Decorator to validate that current user owns the resource
    Useful for ensuring users can only access their own data

    Args:
        model: SQLAlchemy model class
        id_param: URL parameter name containing resource ID
        owner_field: Field in model that contains owner's user_id
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))

            # Get resource ID from kwargs
            resource_id = kwargs.get(id_param)
            if not resource_id:
                abort(404)

            # Get resource from database
            resource = model.query.get(resource_id)
            if not resource:
                abort(404)

            # Check ownership (admin can access everything)
            if current_user.role != 'admin':
                if getattr(resource, owner_field) != current_user.id:
                    flash('You do not have permission to access this resource.', 'danger')
                    abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def ajax_required(f):
    """
    Decorator to ensure request is AJAX
    Useful for API endpoints that should only accept AJAX requests
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_xhr:
            abort(400, 'This endpoint only accepts AJAX requests')
        return f(*args, **kwargs)
    return decorated_function


def rate_limit(max_requests=10, window=60):
    """
    Simple rate limiting decorator
    Args:
        max_requests: Maximum number of requests
        window: Time window in seconds

    Note: This is a basic implementation. For production,
    use Flask-Limiter or similar library
    """
    def decorator(f):
        # Store request counts in memory (not suitable for production)
        request_counts = {}

        @wraps(f)
        def decorated_function(*args, **kwargs):
            from time import time

            # Get client identifier (IP address or user ID)
            if current_user.is_authenticated:
                client_id = current_user.id
            else:
                client_id = request.remote_addr

            current_time = time()

            # Clean old entries
            for key in list(request_counts.keys()):
                if current_time - request_counts[key]['timestamp'] > window:
                    del request_counts[key]

            # Check rate limit
            if client_id in request_counts:
                if request_counts[client_id]['count'] >= max_requests:
                    abort(429, 'Too many requests. Please try again later.')
                request_counts[client_id]['count'] += 1
            else:
                request_counts[client_id] = {
                    'count': 1,
                    'timestamp': current_time
                }

            return f(*args, **kwargs)
        return decorated_function
    return decorator
