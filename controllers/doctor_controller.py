"""
Doctor Controller
Handles doctor dashboard, appointments, treatments, and availability management
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from extensions import db
from models.doctor import Doctor, DoctorAvailability
from models.patient import Patient
from models.appointment import Appointment
from models.treatment import Treatment
from utils.decorators import doctor_required
from utils.helpers import parse_date, parse_time, get_next_n_days, format_date
from datetime import date, time, datetime, timedelta

# Create blueprint
doctor_bp = Blueprint('doctor', __name__)


@doctor_bp.route('/dashboard')
@doctor_required
def dashboard():
    """
    Doctor dashboard
    Shows upcoming appointments, today's schedule, patient count
    """
    # Get doctor profile
    doctor = Doctor.get_by_user_id(current_user.id)

    if not doctor:
        flash('Doctor profile not found. Please contact administrator.', 'danger')
        return redirect(url_for('auth.logout'))

    # Get today's appointments
    today = date.today()
    todays_appointments_list = Appointment.get_today_appointments(doctor_id=doctor.id)

    # Get upcoming appointments (next 7 days)
    upcoming_appointments_list = Appointment.get_upcoming_appointments(days=7, doctor_id=doctor.id)

    # Get recent completed appointments
    completed_appointments_list = Appointment.query.filter_by(
        doctor_id=doctor.id,
        status='Completed'
    ).order_by(Appointment.appointment_date.desc()).limit(10).all()

    # Statistics for stat cards
    today_appointments = len(todays_appointments_list)  # Count for today
    total_patients = len(set(apt.patient_id for apt in Appointment.query.filter_by(doctor_id=doctor.id).all()))  # Unique patients
    completed_appointments = Appointment.query.filter_by(doctor_id=doctor.id, status='Completed').count()
    upcoming_appointments = len(upcoming_appointments_list)

    # Format current date
    current_date = today.strftime('%d %b %Y')

    return render_template('doctor/dashboard.html',
                         doctor=doctor,
                         todays_appointments=todays_appointments_list,
                         today_appointments=today_appointments,
                         total_patients=total_patients,
                         completed_appointments=completed_appointments,
                         upcoming_appointments=upcoming_appointments,
                         current_date=current_date)


# ==================== APPOINTMENT MANAGEMENT ====================

@doctor_bp.route('/appointments')
@doctor_required
def view_appointments():
    """
    View all appointments with filters
    """
    doctor = Doctor.get_by_user_id(current_user.id)

    if not doctor:
        flash('Doctor profile not found.', 'danger')
        return redirect(url_for('auth.logout'))

    # Get filter parameters
    status_filter = request.args.get('status', '')
    date_filter = request.args.get('date', '')

    query = Appointment.query.filter_by(doctor_id=doctor.id)

    # Apply filters
    if status_filter and status_filter in ['Booked', 'Completed', 'Cancelled']:
        query = query.filter_by(status=status_filter)

    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            query = query.filter_by(appointment_date=filter_date)
        except:
            pass

    appointments = query.order_by(
        Appointment.appointment_date.desc(),
        Appointment.appointment_time.desc()
    ).all()

    return render_template('doctor/appointments.html',
                         doctor=doctor,
                         appointments=appointments,
                         status_filter=status_filter,
                         date_filter=date_filter)


@doctor_bp.route('/appointments/<int:appointment_id>')
@doctor_required
def view_appointment(appointment_id):
    """
    View appointment details
    """
    doctor = Doctor.get_by_user_id(current_user.id)
    appointment = Appointment.query.get_or_404(appointment_id)

    # Verify this appointment belongs to the doctor
    if appointment.doctor_id != doctor.id:
        flash('You do not have permission to view this appointment.', 'danger')
        return redirect(url_for('doctor.view_appointments'))

    return render_template('doctor/appointment_detail.html',
                         doctor=doctor,
                         appointment=appointment)


@doctor_bp.route('/appointments/<int:appointment_id>/complete', methods=['GET', 'POST'])
@doctor_required
def complete_appointment(appointment_id):
    """
    Mark appointment as completed and add treatment record
    """
    doctor = Doctor.get_by_user_id(current_user.id)
    appointment = Appointment.query.get_or_404(appointment_id)

    # Verify this appointment belongs to the doctor
    if appointment.doctor_id != doctor.id:
        flash('You do not have permission to modify this appointment.', 'danger')
        return redirect(url_for('doctor.view_appointments'))

    # Check if appointment can be completed
    if not appointment.can_be_completed():
        flash(f'This appointment cannot be completed. Current status: {appointment.status}', 'warning')
        return redirect(url_for('doctor.view_appointment', appointment_id=appointment_id))

    if request.method == 'POST':
        diagnosis = request.form.get('diagnosis', '').strip()
        prescription = request.form.get('prescription', '').strip()
        notes = request.form.get('notes', '').strip()

        # Validation
        if not diagnosis:
            flash('Diagnosis is required.', 'danger')
            return render_template('doctor/complete_appointment.html',
                                 doctor=doctor,
                                 appointment=appointment)

        # Create treatment
        try:
            success, message, treatment = Treatment.create_treatment(
                appointment_id=appointment.id,
                diagnosis=diagnosis,
                prescription=prescription if prescription else None,
                notes=notes if notes else None
            )

            if success:
                flash('Appointment completed and treatment record created successfully!', 'success')
                return redirect(url_for('doctor.view_appointments'))
            else:
                flash(f'Error: {message}', 'danger')

        except Exception as e:
            flash(f'Error completing appointment: {str(e)}', 'danger')

    # GET request
    return render_template('doctor/complete_appointment.html',
                         doctor=doctor,
                         appointment=appointment)


@doctor_bp.route('/appointments/<int:appointment_id>/cancel', methods=['POST'])
@doctor_required
def cancel_appointment(appointment_id):
    """
    Cancel an appointment
    """
    doctor = Doctor.get_by_user_id(current_user.id)
    appointment = Appointment.query.get_or_404(appointment_id)

    # Verify this appointment belongs to the doctor
    if appointment.doctor_id != doctor.id:
        flash('You do not have permission to modify this appointment.', 'danger')
        return redirect(url_for('doctor.view_appointments'))

    # Check if appointment can be cancelled
    if not appointment.can_be_cancelled():
        flash(f'This appointment cannot be cancelled. Current status: {appointment.status}', 'warning')
        return redirect(url_for('doctor.view_appointment', appointment_id=appointment_id))

    reason = request.form.get('reason', 'Cancelled by doctor')

    try:
        appointment.mark_cancelled(reason=reason)
        flash('Appointment cancelled successfully.', 'info')

    except Exception as e:
        flash(f'Error cancelling appointment: {str(e)}', 'danger')

    return redirect(url_for('doctor.view_appointments'))


# ==================== PATIENT HISTORY ====================

@doctor_bp.route('/patients')
@doctor_required
def view_patients():
    """
    View all patients who have appointments with this doctor
    """
    doctor = Doctor.get_by_user_id(current_user.id)

    # Get unique patients from appointments
    patients_query = db.session.query(Patient).join(Appointment).filter(
        Appointment.doctor_id == doctor.id
    ).distinct().order_by(Patient.name).all()

    # Calculate appointment count for each patient with this doctor
    for patient in patients_query:
        patient.appointment_count = Appointment.query.filter_by(
            patient_id=patient.id,
            doctor_id=doctor.id
        ).count()

    return render_template('doctor/patients.html',
                         doctor=doctor,
                         patients=patients_query)


@doctor_bp.route('/patients/<int:patient_id>/history')
@doctor_required
def patient_history(patient_id):
    """
    View patient's complete medical history with this doctor
    """
    doctor = Doctor.get_by_user_id(current_user.id)
    patient = Patient.query.get_or_404(patient_id)

    # Get all appointments between this patient and doctor
    appointments = Appointment.query.filter_by(
        patient_id=patient_id,
        doctor_id=doctor.id
    ).order_by(Appointment.appointment_date.desc()).all()

    # Get treatment records
    treatments = []
    for appointment in appointments:
        if appointment.treatment:
            treatments.append({
                'appointment': appointment,
                'treatment': appointment.treatment
            })

    # Count completed treatments
    completed_count = len(treatments)

    return render_template('doctor/patient_history.html',
                         doctor=doctor,
                         patient=patient,
                         appointments=appointments,
                         treatments=treatments,
                         completed_count=completed_count)


# ==================== AVAILABILITY MANAGEMENT ====================

@doctor_bp.route('/availability')
@doctor_required
def manage_availability():
    """
    View and manage doctor's availability for next 7 days
    """
    doctor = Doctor.get_by_user_id(current_user.id)

    # Get current availability (let template handle grouping)
    availabilities = doctor.get_availability_for_next_7_days()

    # Get next 7 days
    next_7_days = get_next_n_days(7)

    return render_template('doctor/manage_availability.html',
                         doctor=doctor,
                         availabilities=availabilities,
                         next_7_days=next_7_days)


@doctor_bp.route('/availability/add', methods=['GET', 'POST'])
@doctor_required
def add_availability():
    """
    Add availability slot
    """
    doctor = Doctor.get_by_user_id(current_user.id)

    if request.method == 'POST':
        available_date_str = request.form.get('available_date', '')
        start_time_str = request.form.get('start_time', '')
        end_time_str = request.form.get('end_time', '')

        # Validation
        errors = []

        if not available_date_str:
            errors.append('Date is required.')
        if not start_time_str:
            errors.append('Start time is required.')
        if not end_time_str:
            errors.append('End time is required.')

        # Parse date and time
        available_date = parse_date(available_date_str)
        start_time = parse_time(start_time_str)
        end_time = parse_time(end_time_str)

        if not available_date:
            errors.append('Invalid date format.')
        if not start_time:
            errors.append('Invalid start time format.')
        if not end_time:
            errors.append('Invalid end time format.')

        # Check if date is in the future
        if available_date and available_date < date.today():
            errors.append('Cannot set availability for past dates.')

        # Check if date is within next 7 days
        if available_date and available_date > date.today() + timedelta(days=7):
            errors.append('Can only set availability for next 7 days.')

        # Check if end time is after start time
        if start_time and end_time and end_time <= start_time:
            errors.append('End time must be after start time.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            next_7_days = get_next_n_days(7)
            return render_template('doctor/add_availability.html',
                                 doctor=doctor,
                                 next_7_days=next_7_days,
                                 form_data=request.form)

        # Add availability
        try:
            DoctorAvailability.set_doctor_availability(
                doctor_id=doctor.id,
                available_date=available_date,
                start_time=start_time,
                end_time=end_time
            )

            flash('Availability added successfully!', 'success')
            return redirect(url_for('doctor.manage_availability'))

        except Exception as e:
            flash(f'Error adding availability: {str(e)}', 'danger')

    # GET request
    next_7_days = get_next_n_days(7)
    return render_template('doctor/add_availability.html',
                         doctor=doctor,
                         next_7_days=next_7_days)


@doctor_bp.route('/availability/delete/<int:availability_id>', methods=['POST'])
@doctor_required
def delete_availability(availability_id):
    """
    Delete availability slot
    """
    doctor = Doctor.get_by_user_id(current_user.id)
    availability = DoctorAvailability.query.get_or_404(availability_id)

    # Verify this availability belongs to the doctor
    if availability.doctor_id != doctor.id:
        flash('You do not have permission to delete this availability.', 'danger')
        return redirect(url_for('doctor.manage_availability'))

    try:
        db.session.delete(availability)
        db.session.commit()
        flash('Availability slot deleted successfully.', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting availability: {str(e)}', 'danger')

    return redirect(url_for('doctor.manage_availability'))


# ==================== PROFILE ====================

@doctor_bp.route('/profile')
@doctor_required
def profile():
    """
    View doctor's own profile
    """
    doctor = Doctor.get_by_user_id(current_user.id)

    # Calculate statistics for profile page
    total_patients = len(set(apt.patient_id for apt in Appointment.query.filter_by(doctor_id=doctor.id).all()))
    completed_appointments = Appointment.query.filter_by(doctor_id=doctor.id, status='Completed').count()
    upcoming_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.status == 'Booked'
    ).count()

    return render_template('doctor/profile.html',
                         doctor=doctor,
                         total_patients=total_patients,
                         completed_appointments=completed_appointments,
                         upcoming_appointments=upcoming_appointments)


@doctor_bp.route('/profile/edit', methods=['GET', 'POST'])
@doctor_required
def edit_profile():
    """
    Edit doctor's own profile (limited fields)
    """
    doctor = Doctor.get_by_user_id(current_user.id)

    if request.method == 'POST':
        qualification = request.form.get('qualification', '').strip()
        contact_number = request.form.get('contact_number', '').strip()

        # Validation
        if not contact_number:
            flash('Contact number is required.', 'danger')
            return render_template('doctor/edit_profile.html', doctor=doctor)

        # Update profile
        try:
            doctor.qualification = qualification if qualification else None
            doctor.contact_number = contact_number
            db.session.commit()

            flash('Profile updated successfully!', 'success')
            return redirect(url_for('doctor.profile'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error updating profile: {str(e)}', 'danger')

    # GET request
    return render_template('doctor/edit_profile.html', doctor=doctor)
