"""
Patient Controller
Handles patient dashboard, doctor search, appointment booking, and treatment history
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from extensions import db
from models.patient import Patient
from models.doctor import Doctor
from models.specialization import Specialization
from models.appointment import Appointment
from models.treatment import Treatment
from utils.decorators import patient_required
from utils.helpers import parse_date, parse_time, get_next_n_days, format_date, validate_phone
from datetime import date, time, datetime

# Create blueprint
patient_bp = Blueprint('patient', __name__)


@patient_bp.route('/dashboard')
@patient_required
def dashboard():
    """
    Patient dashboard
    Shows available specializations, upcoming appointments, and quick actions
    """
    # Get patient profile
    patient = Patient.get_by_user_id(current_user.id)

    if not patient:
        flash('Patient profile not found. Please contact administrator.', 'danger')
        return redirect(url_for('auth.logout'))

    # Get all specializations
    specializations = Specialization.get_all_specializations()

    # Get upcoming appointments
    upcoming_appointments = patient.upcoming_appointments[:5]  # Next 5

    # Get recent past appointments
    past_appointments = patient.past_appointments[:5]  # Last 5

    # Statistics
    total_appointments = patient.total_appointments
    total_upcoming = len(patient.upcoming_appointments)
    completed_appointments = len(patient.past_appointments)

    return render_template('patient/dashboard.html',
                         patient=patient,
                         specializations=specializations,
                         upcoming_appointments=upcoming_appointments,
                         past_appointments=past_appointments,
                         total_appointments=total_appointments,
                         total_upcoming=total_upcoming,
                         completed_appointments=completed_appointments)


# ==================== DOCTOR SEARCH ====================

@patient_bp.route('/doctors')
@patient_required
def search_doctors():
    """
    Search and browse doctors by specialization or name
    """
    patient = Patient.get_by_user_id(current_user.id)

    # Get filters
    specialization_id = request.args.get('specialization', '')
    search_query = request.args.get('search', '').strip()

    # Get all specializations for filter dropdown
    specializations = Specialization.get_all_specializations()

    # Build query
    if specialization_id:
        doctors = Doctor.get_by_specialization(int(specialization_id))
    elif search_query:
        doctors = Doctor.search(search_query)
    else:
        doctors = Doctor.get_all_doctors()

    return render_template('patient/search_doctors.html',
                         patient=patient,
                         doctors=doctors,
                         specializations=specializations,
                         selected_specialization=specialization_id,
                         search_query=search_query)


@patient_bp.route('/doctors/<int:doctor_id>')
@patient_required
def view_doctor(doctor_id):
    """
    View doctor profile and availability
    """
    patient = Patient.get_by_user_id(current_user.id)
    doctor = Doctor.query.get_or_404(doctor_id)

    # Get doctor's availability for next 7 days
    availability = doctor.get_availability_for_next_7_days()

    # Group availability by date
    availability_by_date = {}
    for slot in availability:
        date_str = format_date(slot.available_date)
        if date_str not in availability_by_date:
            availability_by_date[date_str] = []
        availability_by_date[date_str].append(slot)

    return render_template('patient/view_doctor.html',
                         patient=patient,
                         doctor=doctor,
                         availability_by_date=availability_by_date)


# ==================== APPOINTMENT BOOKING ====================

@patient_bp.route('/appointments/book/<int:doctor_id>', methods=['GET', 'POST'])
@patient_required
def book_appointment(doctor_id):
    """
    Book an appointment with a doctor
    """
    patient = Patient.get_by_user_id(current_user.id)
    doctor = Doctor.query.get_or_404(doctor_id)

    if request.method == 'POST':
        appointment_date_str = request.form.get('appointment_date', '')
        appointment_time_str = request.form.get('appointment_time', '')

        # Validation
        errors = []

        if not appointment_date_str:
            errors.append('Please select an appointment date.')
        if not appointment_time_str:
            errors.append('Please select an appointment time.')

        # Parse date and time
        appointment_date = parse_date(appointment_date_str)
        appointment_time = parse_time(appointment_time_str)

        if not appointment_date:
            errors.append('Invalid date format.')
        if not appointment_time:
            errors.append('Invalid time format.')

        # Check if date is in the future
        if appointment_date and appointment_date < date.today():
            errors.append('Cannot book appointments for past dates.')

        # Check if date is within next 7 days
        from datetime import timedelta
        if appointment_date and appointment_date > date.today() + timedelta(days=7):
            errors.append('Can only book appointments within next 7 days.')

        if errors:
            for error in errors:
                flash(error, 'danger')

            # Get availability for form
            availability = doctor.get_availability_for_next_7_days()
            availability_by_date = {}
            for slot in availability:
                date_str = format_date(slot.available_date)
                if date_str not in availability_by_date:
                    availability_by_date[date_str] = []
                availability_by_date[date_str].append(slot)

            return render_template('patient/book_appointment.html',
                                 patient=patient,
                                 doctor=doctor,
                                 availability_by_date=availability_by_date,
                                 form_data=request.form)

        # Book appointment with double-booking check
        try:
            success, message, appointment = Appointment.create_appointment(
                patient_id=patient.id,
                doctor_id=doctor.id,
                appointment_date=appointment_date,
                appointment_time=appointment_time
            )

            if success:
                flash('Appointment booked successfully!', 'success')
                return redirect(url_for('patient.my_appointments'))
            else:
                flash(f'Error: {message}', 'danger')

                # Get availability for form
                availability = doctor.get_availability_for_next_7_days()
                availability_by_date = {}
                for slot in availability:
                    date_str = format_date(slot.available_date)
                    if date_str not in availability_by_date:
                        availability_by_date[date_str] = []
                    availability_by_date[date_str].append(slot)

                return render_template('patient/book_appointment.html',
                                     patient=patient,
                                     doctor=doctor,
                                     availability_by_date=availability_by_date,
                                     form_data=request.form)

        except Exception as e:
            flash(f'Error booking appointment: {str(e)}', 'danger')

    # GET request - show booking form
    # Get doctor's availability
    availability = doctor.get_availability_for_next_7_days()

    # Group availability by date and convert to JSON-friendly format
    availability_by_date = {}
    availability_json = {}

    for slot in availability:
        # For display in template
        date_str = format_date(slot.available_date)
        if date_str not in availability_by_date:
            availability_by_date[date_str] = []
        availability_by_date[date_str].append(slot)

        # For JavaScript (use ISO format YYYY-MM-DD)
        date_iso = slot.available_date.isoformat()
        if date_iso not in availability_json:
            availability_json[date_iso] = []
        availability_json[date_iso].append({
            'start_time': slot.start_time.strftime('%H:%M'),
            'end_time': slot.end_time.strftime('%H:%M')
        })

    return render_template('patient/book_appointment.html',
                         patient=patient,
                         doctor=doctor,
                         availability_by_date=availability_by_date,
                         availability_json=availability_json)


# ==================== MY APPOINTMENTS ====================

@patient_bp.route('/appointments')
@patient_required
def my_appointments():
    """
    View all patient's appointments
    """
    patient = Patient.get_by_user_id(current_user.id)

    # Get filter
    status_filter = request.args.get('status', '')

    if status_filter and status_filter in ['Booked', 'Completed', 'Cancelled']:
        appointments = Appointment.get_appointments_by_patient(patient.id, status=status_filter)
    else:
        appointments = Appointment.get_appointments_by_patient(patient.id)

    return render_template('patient/my_appointments.html',
                         patient=patient,
                         appointments=appointments,
                         status_filter=status_filter)


@patient_bp.route('/appointments/<int:appointment_id>')
@patient_required
def view_appointment(appointment_id):
    """
    View appointment details
    """
    patient = Patient.get_by_user_id(current_user.id)
    appointment = Appointment.query.get_or_404(appointment_id)

    # Verify this appointment belongs to the patient
    if appointment.patient_id != patient.id:
        flash('You do not have permission to view this appointment.', 'danger')
        return redirect(url_for('patient.my_appointments'))

    return render_template('patient/view_appointment.html',
                         patient=patient,
                         appointment=appointment)


@patient_bp.route('/appointments/<int:appointment_id>/cancel', methods=['POST'])
@patient_required
def cancel_appointment(appointment_id):
    """
    Cancel an appointment
    """
    patient = Patient.get_by_user_id(current_user.id)
    appointment = Appointment.query.get_or_404(appointment_id)

    # Verify this appointment belongs to the patient
    if appointment.patient_id != patient.id:
        flash('You do not have permission to cancel this appointment.', 'danger')
        return redirect(url_for('patient.my_appointments'))

    # Check if appointment can be cancelled
    if not appointment.can_be_cancelled():
        flash(f'This appointment cannot be cancelled. Current status: {appointment.status}', 'warning')
        return redirect(url_for('patient.view_appointment', appointment_id=appointment_id))

    reason = request.form.get('reason', 'Cancelled by patient')

    try:
        appointment.mark_cancelled(reason=reason)
        flash('Appointment cancelled successfully.', 'info')

    except Exception as e:
        flash(f'Error cancelling appointment: {str(e)}', 'danger')

    return redirect(url_for('patient.my_appointments'))


# ==================== TREATMENT HISTORY ====================

@patient_bp.route('/treatment-history')
@patient_required
def treatment_history():
    """
    View complete treatment history
    """
    patient = Patient.get_by_user_id(current_user.id)

    # Get treatment history
    treatments = patient.get_treatment_history()

    # Calculate statistics
    total_treatments = len(treatments)
    unique_doctors = len(set(t.appointment.doctor_id for t in treatments)) if treatments else 0
    unique_specializations = len(set(t.appointment.doctor.specialization_id for t in treatments)) if treatments else 0

    return render_template('patient/treatment_history.html',
                         patient=patient,
                         treatments=treatments,
                         total_treatments=total_treatments,
                         unique_doctors=unique_doctors,
                         unique_specializations=unique_specializations)


@patient_bp.route('/treatment/<int:treatment_id>')
@patient_required
def view_treatment(treatment_id):
    """
    View detailed treatment record
    """
    patient = Patient.get_by_user_id(current_user.id)
    treatment = Treatment.query.get_or_404(treatment_id)

    # Verify this treatment belongs to the patient
    if treatment.appointment.patient_id != patient.id:
        flash('You do not have permission to view this treatment record.', 'danger')
        return redirect(url_for('patient.treatment_history'))

    return render_template('patient/view_treatment.html',
                         patient=patient,
                         treatment=treatment,
                         appointment=treatment.appointment)


# ==================== PROFILE MANAGEMENT ====================

@patient_bp.route('/profile')
@patient_required
def profile():
    """
    View patient's own profile
    """
    patient = Patient.get_by_user_id(current_user.id)

    return render_template('patient/profile.html', patient=patient)


@patient_bp.route('/profile/edit', methods=['GET', 'POST'])
@patient_required
def edit_profile():
    """
    Edit patient's own profile
    """
    patient = Patient.get_by_user_id(current_user.id)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        contact_number = request.form.get('contact_number', '').strip()
        address = request.form.get('address', '').strip()
        blood_group = request.form.get('blood_group', '')
        emergency_contact = request.form.get('emergency_contact', '').strip()

        # Validation
        errors = []

        if not name:
            errors.append('Name is required.')
        if not contact_number:
            errors.append('Contact number is required.')

        # Validate phone
        if contact_number and not validate_phone(contact_number):
            errors.append('Please enter a valid 10-digit phone number.')

        # Validate blood group
        if blood_group and not Patient.validate_blood_group(blood_group):
            errors.append('Please enter a valid blood group.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('patient/edit_profile.html',
                                 patient=patient,
                                 form_data=request.form)

        # Update profile
        try:
            patient.name = name
            patient.contact_number = contact_number
            patient.address = address if address else None
            patient.blood_group = blood_group if blood_group else None
            patient.emergency_contact = emergency_contact if emergency_contact else None

            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('patient.profile'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error updating profile: {str(e)}', 'danger')

    # GET request
    return render_template('patient/edit_profile.html', patient=patient)


# ==================== SPECIALIZATIONS ====================

@patient_bp.route('/specializations')
@patient_required
def view_specializations():
    """
    View all available specializations
    """
    patient = Patient.get_by_user_id(current_user.id)
    specializations = Specialization.get_all_specializations()

    return render_template('patient/specializations.html',
                         patient=patient,
                         specializations=specializations)


@patient_bp.route('/specializations/<int:specialization_id>/doctors')
@patient_required
def doctors_by_specialization(specialization_id):
    """
    View all doctors in a specific specialization
    """
    patient = Patient.get_by_user_id(current_user.id)
    specialization = Specialization.query.get_or_404(specialization_id)
    doctors = Doctor.get_by_specialization(specialization_id)

    return render_template('patient/doctors_by_specialization.html',
                         patient=patient,
                         specialization=specialization,
                         doctors=doctors)
