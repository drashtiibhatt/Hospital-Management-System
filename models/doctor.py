"""
Doctor Model
Represents medical professionals in the hospital
"""

from datetime import datetime, date, timedelta
from extensions import db


class Doctor(db.Model):
    """
    Doctor model for medical professionals
    Linked to User model via user_id
    """

    __tablename__ = 'doctors'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign Key to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    # Foreign Key to Specialization
    specialization_id = db.Column(db.Integer, db.ForeignKey('specializations.id'), nullable=False)

    # Doctor details
    name = db.Column(db.String(100), nullable=False, index=True)
    license_number = db.Column(db.String(50), nullable=True, unique=True)
    qualification = db.Column(db.String(200), nullable=True)
    experience_years = db.Column(db.Integer, nullable=True)
    contact_number = db.Column(db.String(15), nullable=True)
    profile_image = db.Column(db.String(255), nullable=True)

    # Relationships
    appointments = db.relationship('Appointment', backref='doctor', lazy='dynamic', cascade='all, delete-orphan')
    availability_slots = db.relationship('DoctorAvailability', backref='doctor', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, user_id, name, specialization_id, license_number=None,
                 qualification=None, experience_years=None, contact_number=None):
        """Initialize a new Doctor"""
        self.user_id = user_id
        self.name = name
        self.specialization_id = specialization_id
        self.license_number = license_number
        self.qualification = qualification
        self.experience_years = experience_years
        self.contact_number = contact_number

    def __repr__(self):
        """String representation of Doctor"""
        return f'<Doctor {self.name} - {self.specialization.name if self.specialization else "Unknown"}>'

    @property
    def total_appointments(self):
        """Get total number of appointments"""
        return self.appointments.count()

    @property
    def upcoming_appointments(self):
        """Get upcoming appointments (today onwards)"""
        from models.appointment import Appointment
        today = date.today()
        return self.appointments.filter(
            Appointment.appointment_date >= today,
            Appointment.status == 'Booked'
        ).order_by(Appointment.appointment_date, Appointment.appointment_time).all()

    def get_availability_for_next_7_days(self):
        """Get availability for next 7 days"""
        today = date.today()
        end_date = today + timedelta(days=7)

        return DoctorAvailability.query.filter(
            DoctorAvailability.doctor_id == self.id,
            DoctorAvailability.available_date >= today,
            DoctorAvailability.available_date <= end_date,
            DoctorAvailability.is_available == True
        ).order_by(DoctorAvailability.available_date, DoctorAvailability.start_time).all()

    def is_available_on(self, check_date, check_time):
        """Check if doctor is available on specific date and time"""
        availability = DoctorAvailability.query.filter_by(
            doctor_id=self.id,
            available_date=check_date,
            is_available=True
        ).all()

        for slot in availability:
            if slot.start_time <= check_time <= slot.end_time:
                return True
        return False

    def to_dict(self, include_availability=False):
        """Convert doctor to dictionary (for API responses)"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'license_number': self.license_number,
            'specialization': self.specialization.name if self.specialization else None,
            'specialization_id': self.specialization_id,
            'qualification': self.qualification,
            'experience_years': self.experience_years,
            'contact_number': self.contact_number,
            'profile_image': self.profile_image,
            'total_appointments': self.total_appointments,
            'username': self.user.username if self.user else None,
            'email': self.user.email if self.user else None
        }

        if include_availability:
            data['availability'] = [
                avail.to_dict() for avail in self.get_availability_for_next_7_days()
            ]

        return data

    @staticmethod
    def get_by_user_id(user_id):
        """Get doctor by user ID"""
        return Doctor.query.filter_by(user_id=user_id).first()

    @staticmethod
    def get_by_specialization(specialization_id):
        """Get all doctors by specialization"""
        return Doctor.query.filter_by(specialization_id=specialization_id).all()

    @staticmethod
    def search(query):
        """Search doctors by name"""
        return Doctor.query.filter(Doctor.name.ilike(f'%{query}%')).all()

    @staticmethod
    def get_all_doctors():
        """Get all doctors"""
        return Doctor.query.order_by(Doctor.name).all()


class DoctorAvailability(db.Model):
    """
    Doctor Availability model
    Stores doctor availability for next 7 days
    """

    __tablename__ = 'doctor_availability'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign Key to Doctor
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)

    # Availability details
    available_date = db.Column(db.Date, nullable=False, index=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_available = db.Column(db.Boolean, default=True, nullable=False)

    # Composite index for efficient querying
    __table_args__ = (
        db.Index('idx_doctor_date', 'doctor_id', 'available_date'),
    )

    def __init__(self, doctor_id, available_date, start_time, end_time, is_available=True):
        """Initialize a new DoctorAvailability slot"""
        self.doctor_id = doctor_id
        self.available_date = available_date
        self.start_time = start_time
        self.end_time = end_time
        self.is_available = is_available

    def __repr__(self):
        """String representation of DoctorAvailability"""
        return f'<DoctorAvailability Doctor:{self.doctor_id} Date:{self.available_date}>'

    def to_dict(self):
        """Convert availability to dictionary"""
        return {
            'id': self.id,
            'doctor_id': self.doctor_id,
            'available_date': self.available_date.isoformat() if self.available_date else None,
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'is_available': self.is_available
        }

    @staticmethod
    def set_doctor_availability(doctor_id, available_date, start_time, end_time):
        """Set or update doctor availability for a specific date"""
        # Check if availability already exists
        existing = DoctorAvailability.query.filter_by(
            doctor_id=doctor_id,
            available_date=available_date,
            start_time=start_time
        ).first()

        if existing:
            existing.end_time = end_time
            existing.is_available = True
        else:
            new_availability = DoctorAvailability(
                doctor_id=doctor_id,
                available_date=available_date,
                start_time=start_time,
                end_time=end_time
            )
            db.session.add(new_availability)

        db.session.commit()

    @staticmethod
    def remove_past_availability():
        """Remove availability slots for dates before today"""
        today = date.today()
        DoctorAvailability.query.filter(
            DoctorAvailability.available_date < today
        ).delete()
        db.session.commit()
