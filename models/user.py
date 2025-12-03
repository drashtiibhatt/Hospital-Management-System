"""
User Model
Base authentication model for all users (Admin, Doctor, Patient)
"""

from datetime import datetime
from flask_login import UserMixin
from extensions import db


class User(UserMixin, db.Model):
    """
    User model for authentication
    Serves as base table for all user types (Admin, Doctor, Patient)
    """

    __tablename__ = 'users'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Authentication fields
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # User role (admin, doctor, patient)
    role = db.Column(db.String(20), nullable=False, index=True)

    # Account status
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships (one-to-one with role-specific tables)
    admin = db.relationship('Admin', backref='user', uselist=False, cascade='all, delete-orphan')
    doctor = db.relationship('Doctor', backref='user', uselist=False, cascade='all, delete-orphan')
    patient = db.relationship('Patient', backref='user', uselist=False, cascade='all, delete-orphan')

    def __init__(self, username, email, password_hash, role):
        """Initialize a new User"""
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.is_active = True

    def __repr__(self):
        """String representation of User"""
        return f'<User {self.username} ({self.role})>'

    # Flask-Login required methods
    def get_id(self):
        """Return user ID as string (required by Flask-Login)"""
        return str(self.id)

    @property
    def is_authenticated(self):
        """Return True if user is authenticated"""
        return True

    @property
    def is_anonymous(self):
        """Return False as this is not an anonymous user"""
        return False

    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'

    def is_doctor(self):
        """Check if user is doctor"""
        return self.role == 'doctor'

    def is_patient(self):
        """Check if user is patient"""
        return self.role == 'patient'

    def to_dict(self):
        """Convert user to dictionary (for API responses)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    @staticmethod
    def validate_role(role):
        """Validate user role"""
        valid_roles = ['admin', 'doctor', 'patient']
        return role.lower() in valid_roles

    def deactivate(self):
        """Deactivate user account (blacklist)"""
        self.is_active = False
        db.session.commit()

    def activate(self):
        """Activate user account"""
        self.is_active = True
        db.session.commit()
