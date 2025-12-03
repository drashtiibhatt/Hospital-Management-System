"""
Patient Model
Represents patients seeking medical care
"""

from datetime import datetime, date
from extensions import db


class Patient(db.Model):
    """
    Patient model for individuals seeking medical care
    Linked to User model via user_id
    """

    __tablename__ = 'patients'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign Key to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    # Patient details
    name = db.Column(db.String(100), nullable=False, index=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    contact_number = db.Column(db.String(15), nullable=False)
    address = db.Column(db.Text, nullable=True)
    blood_group = db.Column(db.String(5), nullable=True)
    emergency_contact = db.Column(db.String(15), nullable=True)

    # Relationships
    appointments = db.relationship('Appointment', backref='patient', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, user_id, name, contact_number, date_of_birth=None,
                 gender=None, address=None, blood_group=None, emergency_contact=None):
        """Initialize a new Patient"""
        self.user_id = user_id
        self.name = name
        self.contact_number = contact_number
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.address = address
        self.blood_group = blood_group
        self.emergency_contact = emergency_contact

    def __repr__(self):
        """String representation of Patient"""
        return f'<Patient {self.name}>'

    @property
    def age(self):
        """Calculate patient age from date of birth"""
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year
            # Adjust if birthday hasn't occurred this year
            if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
                age -= 1
            return age
        return None

    @property
    def total_appointments(self):
        """Get total number of appointments"""
        return self.appointments.count()

    @property
    def upcoming_appointments(self):
        """Get upcoming appointments"""
        from models.appointment import Appointment
        today = date.today()
        return self.appointments.filter(
            Appointment.appointment_date >= today,
            Appointment.status == 'Booked'
        ).order_by(Appointment.appointment_date, Appointment.appointment_time).all()

    @property
    def past_appointments(self):
        """Get past appointments"""
        from models.appointment import Appointment
        today = date.today()
        return self.appointments.filter(
            db.or_(
                Appointment.appointment_date < today,
                Appointment.status.in_(['Completed', 'Cancelled'])
            )
        ).order_by(Appointment.appointment_date.desc(), Appointment.appointment_time.desc()).all()

    def get_treatment_history(self):
        """Get complete treatment history"""
        from models.treatment import Treatment

        # Get all treatments for this patient's appointments
        treatments = Treatment.query.join(Treatment.appointment).filter(
            Treatment.appointment.has(patient_id=self.id)
        ).order_by(Treatment.treatment_date.desc()).all()

        return treatments

    def to_dict(self, include_appointments=False):
        """Convert patient to dictionary (for API responses)"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'age': self.age,
            'gender': self.gender,
            'contact_number': self.contact_number,
            'address': self.address,
            'blood_group': self.blood_group,
            'emergency_contact': self.emergency_contact,
            'total_appointments': self.total_appointments,
            'username': self.user.username if self.user else None,
            'email': self.user.email if self.user else None
        }

        if include_appointments:
            data['upcoming_appointments'] = [
                apt.to_dict() for apt in self.upcoming_appointments
            ]
            data['past_appointments'] = [
                apt.to_dict() for apt in self.past_appointments[:10]  # Last 10
            ]

        return data

    @staticmethod
    def get_by_user_id(user_id):
        """Get patient by user ID"""
        return Patient.query.filter_by(user_id=user_id).first()

    @staticmethod
    def search(query):
        """Search patients by name or contact number"""
        return Patient.query.filter(
            db.or_(
                Patient.name.ilike(f'%{query}%'),
                Patient.contact_number.ilike(f'%{query}%')
            )
        ).all()

    @staticmethod
    def get_all_patients():
        """Get all patients"""
        return Patient.query.order_by(Patient.name).all()

    @staticmethod
    def validate_blood_group(blood_group):
        """Validate blood group"""
        valid_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        return blood_group.upper() in valid_groups

    @staticmethod
    def validate_gender(gender):
        """Validate gender"""
        valid_genders = ['Male', 'Female', 'Other']
        return gender in valid_genders
