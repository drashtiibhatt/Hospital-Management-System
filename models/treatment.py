"""
Treatment Model
Represents medical treatment records for completed appointments
"""

from datetime import datetime
from extensions import db


class Treatment(db.Model):
    """
    Treatment model for medical records
    Created when doctor marks appointment as completed
    One-to-one relationship with Appointment
    """

    __tablename__ = 'treatments'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign Key to Appointment (one-to-one)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), unique=True, nullable=False)

    # Treatment details
    diagnosis = db.Column(db.Text, nullable=False)
    prescription = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    # Timestamp
    treatment_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, appointment_id, diagnosis, prescription=None, notes=None):
        """Initialize a new Treatment record"""
        self.appointment_id = appointment_id
        self.diagnosis = diagnosis
        self.prescription = prescription
        self.notes = notes

    def __repr__(self):
        """String representation of Treatment"""
        return f'<Treatment for Appointment:{self.appointment_id}>'

    def to_dict(self):
        """Convert treatment to dictionary (for API responses)"""
        return {
            'id': self.id,
            'appointment_id': self.appointment_id,
            'diagnosis': self.diagnosis,
            'prescription': self.prescription,
            'notes': self.notes,
            'treatment_date': self.treatment_date.isoformat() if self.treatment_date else None,
            'doctor_name': self.appointment.doctor.name if self.appointment and self.appointment.doctor else None,
            'patient_name': self.appointment.patient.name if self.appointment and self.appointment.patient else None,
            'appointment_date': self.appointment.appointment_date.isoformat() if self.appointment else None
        }

    def update_treatment(self, diagnosis=None, prescription=None, notes=None):
        """Update treatment details"""
        if diagnosis:
            self.diagnosis = diagnosis
        if prescription:
            self.prescription = prescription
        if notes:
            self.notes = notes

        self.updated_at = datetime.utcnow()
        db.session.commit()

    @staticmethod
    def create_treatment(appointment_id, diagnosis, prescription=None, notes=None):
        """
        Create a new treatment record and mark appointment as completed
        Returns (success: bool, message: str, treatment: Treatment or None)
        """
        from models.appointment import Appointment

        # Check if appointment exists
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return False, "Appointment not found.", None

        # Check if appointment can be completed
        if not appointment.can_be_completed():
            return False, f"Appointment cannot be completed. Current status: {appointment.status}", None

        # Check if treatment already exists
        existing_treatment = Treatment.query.filter_by(appointment_id=appointment_id).first()
        if existing_treatment:
            return False, "Treatment record already exists for this appointment.", None

        try:
            # Create treatment record
            treatment = Treatment(
                appointment_id=appointment_id,
                diagnosis=diagnosis,
                prescription=prescription,
                notes=notes
            )
            db.session.add(treatment)

            # Mark appointment as completed
            appointment.mark_completed()

            db.session.commit()
            return True, "Treatment record created successfully!", treatment

        except Exception as e:
            db.session.rollback()
            return False, f"Error creating treatment: {str(e)}", None

    @staticmethod
    def get_treatment_by_appointment(appointment_id):
        """Get treatment record by appointment ID"""
        return Treatment.query.filter_by(appointment_id=appointment_id).first()

    @staticmethod
    def get_patient_treatment_history(patient_id):
        """Get all treatment records for a patient"""
        from models.appointment import Appointment

        treatments = Treatment.query.join(Appointment).filter(
            Appointment.patient_id == patient_id
        ).order_by(Treatment.treatment_date.desc()).all()

        return treatments

    @staticmethod
    def get_doctor_treatments(doctor_id):
        """Get all treatments provided by a doctor"""
        from models.appointment import Appointment

        treatments = Treatment.query.join(Appointment).filter(
            Appointment.doctor_id == doctor_id
        ).order_by(Treatment.treatment_date.desc()).all()

        return treatments

    @staticmethod
    def search_by_diagnosis(query):
        """Search treatments by diagnosis"""
        return Treatment.query.filter(
            Treatment.diagnosis.ilike(f'%{query}%')
        ).all()
