"""
Appointment Model
Represents scheduled appointments between patients and doctors
"""

from datetime import datetime, date
from extensions import db


class Appointment(db.Model):
    """
    Appointment model for booking consultations
    Links patients with doctors at specific date/time
    """

    __tablename__ = 'appointments'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign Keys
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False, index=True)

    # Appointment details
    appointment_date = db.Column(db.Date, nullable=False, index=True)
    appointment_time = db.Column(db.Time, nullable=False)

    # Status: Booked, Completed, Cancelled
    status = db.Column(db.String(20), default='Booked', nullable=False, index=True)

    # Timestamps
    booking_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Cancellation details
    cancellation_reason = db.Column(db.Text, nullable=True)

    # Relationships
    treatment = db.relationship('Treatment', backref='appointment', uselist=False, cascade='all, delete-orphan')

    # Composite index and unique constraint for preventing double-booking
    __table_args__ = (
        db.Index('idx_doctor_date_time', 'doctor_id', 'appointment_date', 'appointment_time'),
    )

    def __init__(self, patient_id, doctor_id, appointment_date, appointment_time, status='Booked'):
        """Initialize a new Appointment"""
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.status = status

    def __repr__(self):
        """String representation of Appointment"""
        return f'<Appointment {self.id} - Patient:{self.patient_id} Doctor:{self.doctor_id} {self.status}>'

    @property
    def is_upcoming(self):
        """Check if appointment is in the future"""
        today = date.today()
        return self.appointment_date >= today and self.status == 'Booked'

    @property
    def is_past(self):
        """Check if appointment is in the past"""
        today = date.today()
        return self.appointment_date < today or self.status in ['Completed', 'Cancelled']

    def mark_completed(self):
        """Mark appointment as completed"""
        self.status = 'Completed'
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def mark_cancelled(self, reason=None):
        """Mark appointment as cancelled"""
        self.status = 'Cancelled'
        self.cancellation_reason = reason
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def can_be_cancelled(self):
        """Check if appointment can be cancelled"""
        # Can only cancel if status is Booked
        return self.status == 'Booked'

    def can_be_completed(self):
        """Check if appointment can be marked as completed"""
        # Can only complete if status is Booked
        return self.status == 'Booked'

    def to_dict(self, include_treatment=False):
        """Convert appointment to dictionary (for API responses)"""
        data = {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': self.patient.name if self.patient else None,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.name if self.doctor else None,
            'specialization': self.doctor.specialization.name if self.doctor and self.doctor.specialization else None,
            'appointment_date': self.appointment_date.isoformat() if self.appointment_date else None,
            'appointment_time': self.appointment_time.strftime('%H:%M') if self.appointment_time else None,
            'status': self.status,
            'booking_date': self.booking_date.isoformat() if self.booking_date else None,
            'cancellation_reason': self.cancellation_reason
        }

        if include_treatment and self.treatment:
            data['treatment'] = self.treatment.to_dict()

        return data

    @staticmethod
    def check_double_booking(doctor_id, appointment_date, appointment_time):
        """
        Check if doctor already has an appointment at the same date/time
        Returns True if time slot is available, False if already booked
        """
        existing = Appointment.query.filter_by(
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status='Booked'
        ).first()

        return existing is None  # True if available, False if booked

    @staticmethod
    def create_appointment(patient_id, doctor_id, appointment_date, appointment_time):
        """
        Create a new appointment with double-booking check
        Returns (success: bool, message: str, appointment: Appointment or None)
        """
        # Check for double-booking
        if not Appointment.check_double_booking(doctor_id, appointment_date, appointment_time):
            return False, "Doctor is not available at this time. Please choose another time slot.", None

        # Check if doctor has availability set for this date/time
        from models.doctor import Doctor
        doctor = Doctor.query.get(doctor_id)
        if doctor and not doctor.is_available_on(appointment_date, appointment_time):
            return False, "Doctor is not available on this date/time. Please check availability.", None

        # Create appointment
        try:
            appointment = Appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                appointment_date=appointment_date,
                appointment_time=appointment_time
            )
            db.session.add(appointment)
            db.session.commit()
            return True, "Appointment booked successfully!", appointment

        except Exception as e:
            db.session.rollback()
            return False, f"Error creating appointment: {str(e)}", None

    @staticmethod
    def get_appointments_by_doctor(doctor_id, status=None, from_date=None):
        """Get appointments for a specific doctor"""
        query = Appointment.query.filter_by(doctor_id=doctor_id)

        if status:
            query = query.filter_by(status=status)

        if from_date:
            query = query.filter(Appointment.appointment_date >= from_date)

        return query.order_by(Appointment.appointment_date, Appointment.appointment_time).all()

    @staticmethod
    def get_appointments_by_patient(patient_id, status=None):
        """Get appointments for a specific patient"""
        query = Appointment.query.filter_by(patient_id=patient_id)

        if status:
            query = query.filter_by(status=status)

        return query.order_by(Appointment.appointment_date.desc(), Appointment.appointment_time.desc()).all()

    @staticmethod
    def get_all_appointments(status=None, from_date=None, to_date=None):
        """Get all appointments with optional filters"""
        query = Appointment.query

        if status:
            query = query.filter_by(status=status)

        if from_date:
            query = query.filter(Appointment.appointment_date >= from_date)

        if to_date:
            query = query.filter(Appointment.appointment_date <= to_date)

        return query.order_by(Appointment.appointment_date.desc(), Appointment.appointment_time.desc()).all()

    @staticmethod
    def get_today_appointments(doctor_id=None):
        """Get appointments for today"""
        today = date.today()
        query = Appointment.query.filter_by(appointment_date=today, status='Booked')

        if doctor_id:
            query = query.filter_by(doctor_id=doctor_id)

        return query.order_by(Appointment.appointment_time).all()

    @staticmethod
    def get_upcoming_appointments(days=7, doctor_id=None):
        """Get upcoming appointments for next N days"""
        from datetime import timedelta
        today = date.today()
        end_date = today + timedelta(days=days)

        query = Appointment.query.filter(
            Appointment.appointment_date >= today,
            Appointment.appointment_date <= end_date,
            Appointment.status == 'Booked'
        )

        if doctor_id:
            query = query.filter_by(doctor_id=doctor_id)

        return query.order_by(Appointment.appointment_date, Appointment.appointment_time).all()

    @staticmethod
    def validate_status(status):
        """Validate appointment status"""
        valid_statuses = ['Booked', 'Completed', 'Cancelled']
        return status in valid_statuses
