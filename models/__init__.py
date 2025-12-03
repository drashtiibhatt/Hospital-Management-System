"""
Models package
Contains all database models for the Hospital Management System
"""

# Import all models to make them available when importing the models package
from models.user import User
from models.admin import Admin
from models.doctor import Doctor
from models.patient import Patient
from models.specialization import Specialization
from models.appointment import Appointment
from models.treatment import Treatment

__all__ = [
    'User',
    'Admin',
    'Doctor',
    'Patient',
    'Specialization',
    'Appointment',
    'Treatment'
]
