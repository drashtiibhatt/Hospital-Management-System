"""
Admin Controller
Handles all admin operations: dashboard, manage doctors, patients, appointments
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from extensions import db, bcrypt
from models.user import User
from models.admin import Admin
from models.doctor import Doctor
from models.patient import Patient
from models.specialization import Specialization
from models.appointment import Appointment
from utils.decorators import admin_required
from utils.helpers import validate_email, validate_phone, sanitize_string
from datetime import datetime, date

# Create blueprint
admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """
    Admin dashboard with statistics
    Shows total doctors, patients, appointments
    """
    # Get statistics
    total_doctors = Doctor.query.count()
    total_patients = Patient.query.count()
    total_appointments = Appointment.query.count()
    booked_appointments = Appointment.query.filter_by(status='Booked').count()
    completed_appointments = Appointment.query.filter_by(status='Completed').count()
    cancelled_appointments = Appointment.query.filter_by(status='Cancelled').count()
    total_specializations = Specialization.query.count()

    # Get recent appointments
    recent_appointments = Appointment.query.order_by(
        Appointment.booking_date.desc()
    ).limit(10).all()

    # Get today's appointments (pending/booked for today)
    today = date.today()
    pending_appointments = Appointment.query.filter_by(
        appointment_date=today,
        status='Booked'
    ).count()

    # Get specializations list for display
    specializations = Specialization.query.order_by(Specialization.name).all()

    return render_template('admin/dashboard.html',
                         total_doctors=total_doctors,
                         total_patients=total_patients,
                         total_appointments=total_appointments,
                         booked_appointments=booked_appointments,
                         completed_appointments=completed_appointments,
                         cancelled_appointments=cancelled_appointments,
                         total_specializations=total_specializations,
                         recent_appointments=recent_appointments,
                         pending_appointments=pending_appointments,
                         specializations=specializations)


# ==================== DOCTOR MANAGEMENT ====================

@admin_bp.route('/doctors')
@admin_required
def manage_doctors():
    """
    View all doctors
    """
    search_query = request.args.get('search', '').strip()

    if search_query:
        # Search doctors by name or specialization
        doctors = Doctor.query.join(Specialization).filter(
            db.or_(
                Doctor.name.ilike(f'%{search_query}%'),
                Specialization.name.ilike(f'%{search_query}%')
            )
        ).order_by(Doctor.name).all()
    else:
        doctors = Doctor.get_all_doctors()

    return render_template('admin/manage_doctors.html',
                         doctors=doctors,
                         search_query=search_query)


@admin_bp.route('/doctors/add', methods=['GET', 'POST'])
@admin_required
def add_doctor():
    """
    Add a new doctor
    """
    if request.method == 'POST':
        # Get form data
        username = sanitize_string(request.form.get('username', ''), max_length=80)
        email = sanitize_string(request.form.get('email', ''), max_length=120)
        password = request.form.get('password', '')
        name = sanitize_string(request.form.get('name', ''), max_length=100)
        license_number = sanitize_string(request.form.get('license_number', ''), max_length=50)
        specialization_id = request.form.get('specialization_id', '')
        qualification = sanitize_string(request.form.get('qualification', ''), max_length=200)
        experience_years = request.form.get('experience_years', '')
        contact_number = sanitize_string(request.form.get('contact_number', ''), max_length=15)

        # Validation
        errors = []

        if not username:
            errors.append('Username is required.')
        if not email:
            errors.append('Email is required.')
        if not password:
            errors.append('Password is required.')
        if not name:
            errors.append('Doctor name is required.')
        if not specialization_id:
            errors.append('Specialization is required.')
        if not contact_number:
            errors.append('Contact number is required.')

        # Validate email
        if email and not validate_email(email):
            errors.append('Please enter a valid email address.')

        # Validate phone
        if contact_number and not validate_phone(contact_number):
            errors.append('Please enter a valid 10-digit phone number.')

        # Check username uniqueness
        if User.query.filter_by(username=username).first():
            errors.append('Username already exists.')

        # Check email uniqueness
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered.')

        # Password length
        if len(password) < 6:
            errors.append('Password must be at least 6 characters long.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            specializations = Specialization.get_all_specializations()
            return render_template('admin/add_doctor.html',
                                 specializations=specializations,
                                 form_data=request.form)

        # Create doctor
        try:
            # Hash password
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

            # Create user
            user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                role='doctor'
            )
            db.session.add(user)
            db.session.flush()

            # Create doctor profile
            doctor = Doctor(
                user_id=user.id,
                name=name,
                specialization_id=int(specialization_id),
                license_number=license_number if license_number else None,
                qualification=qualification if qualification else None,
                experience_years=int(experience_years) if experience_years else None,
                contact_number=contact_number
            )
            db.session.add(doctor)
            db.session.commit()

            flash(f'Doctor {name} added successfully!', 'success')
            return redirect(url_for('admin.manage_doctors'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error adding doctor: {str(e)}', 'danger')

    # GET request
    specializations = Specialization.get_all_specializations()
    return render_template('admin/add_doctor.html', specializations=specializations)


@admin_bp.route('/doctors/edit/<int:doctor_id>', methods=['GET', 'POST'])
@admin_required
def edit_doctor(doctor_id):
    """
    Edit doctor information
    """
    doctor = Doctor.query.get_or_404(doctor_id)

    if request.method == 'POST':
        # Get form data
        name = sanitize_string(request.form.get('name', ''), max_length=100)
        license_number = sanitize_string(request.form.get('license_number', ''), max_length=50)
        specialization_id = request.form.get('specialization_id', '')
        qualification = sanitize_string(request.form.get('qualification', ''), max_length=200)
        experience_years = request.form.get('experience_years', '')
        contact_number = sanitize_string(request.form.get('contact_number', ''), max_length=15)
        email = sanitize_string(request.form.get('email', ''), max_length=120)

        # Validation
        errors = []

        if not name:
            errors.append('Doctor name is required.')
        if not specialization_id:
            errors.append('Specialization is required.')
        if not contact_number:
            errors.append('Contact number is required.')

        # Validate email
        if email and not validate_email(email):
            errors.append('Please enter a valid email address.')

        # Validate phone
        if contact_number and not validate_phone(contact_number):
            errors.append('Please enter a valid 10-digit phone number.')

        # Check email uniqueness (excluding current doctor)
        existing_email = User.query.filter_by(email=email).first()
        if existing_email and existing_email.id != doctor.user_id:
            errors.append('Email already registered to another user.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            specializations = Specialization.get_all_specializations()
            return render_template('admin/edit_doctor.html',
                                 doctor=doctor,
                                 specializations=specializations)

        # Update doctor
        try:
            doctor.name = name
            doctor.license_number = license_number if license_number else None
            doctor.specialization_id = int(specialization_id)
            doctor.qualification = qualification if qualification else None
            doctor.experience_years = int(experience_years) if experience_years else None
            doctor.contact_number = contact_number

            # Update user email
            doctor.user.email = email

            db.session.commit()
            flash(f'Doctor {name} updated successfully!', 'success')
            return redirect(url_for('admin.manage_doctors'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error updating doctor: {str(e)}', 'danger')

    # GET request
    specializations = Specialization.get_all_specializations()
    return render_template('admin/edit_doctor.html',
                         doctor=doctor,
                         specializations=specializations)


@admin_bp.route('/doctors/delete/<int:doctor_id>', methods=['POST'])
@admin_required
def delete_doctor(doctor_id):
    """
    Delete a doctor
    """
    doctor = Doctor.query.get_or_404(doctor_id)

    try:
        doctor_name = doctor.name
        user = doctor.user

        # Delete doctor (cascade will delete appointments and treatments)
        db.session.delete(doctor)
        db.session.delete(user)
        db.session.commit()

        flash(f'Doctor {doctor_name} deleted successfully.', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting doctor: {str(e)}', 'danger')

    return redirect(url_for('admin.manage_doctors'))


@admin_bp.route('/doctors/toggle-active/<int:doctor_id>', methods=['POST'])
@admin_required
def toggle_doctor_active(doctor_id):
    """
    Activate or deactivate a doctor account
    """
    doctor = Doctor.query.get_or_404(doctor_id)

    try:
        if doctor.user.is_active:
            doctor.user.deactivate()
            flash(f'Doctor {doctor.name} has been deactivated.', 'warning')
        else:
            doctor.user.activate()
            flash(f'Doctor {doctor.name} has been activated.', 'success')

    except Exception as e:
        flash(f'Error toggling doctor status: {str(e)}', 'danger')

    return redirect(url_for('admin.manage_doctors'))


# ==================== PATIENT MANAGEMENT ====================

@admin_bp.route('/patients')
@admin_required
def manage_patients():
    """
    View all patients
    """
    search_query = request.args.get('search', '').strip()

    if search_query:
        # Search patients by name, contact, or ID
        patients = Patient.query.filter(
            db.or_(
                Patient.name.ilike(f'%{search_query}%'),
                Patient.contact_number.ilike(f'%{search_query}%'),
                Patient.id.like(f'%{search_query}%')
            )
        ).order_by(Patient.name).all()
    else:
        patients = Patient.get_all_patients()

    return render_template('admin/manage_patients.html',
                         patients=patients,
                         search_query=search_query)


@admin_bp.route('/patients/view/<int:patient_id>')
@admin_required
def view_patient(patient_id):
    """
    View patient details and history
    """
    patient = Patient.query.get_or_404(patient_id)
    appointments = patient.appointments.order_by(
        Appointment.appointment_date.desc(),
        Appointment.appointment_time.desc()
    ).all()
    treatment_history = patient.get_treatment_history()

    return render_template('admin/view_patient.html',
                         patient=patient,
                         appointments=appointments,
                         treatment_history=treatment_history)


@admin_bp.route('/patients/edit/<int:patient_id>', methods=['GET', 'POST'])
@admin_required
def edit_patient(patient_id):
    """
    Edit patient information
    """
    patient = Patient.query.get_or_404(patient_id)

    if request.method == 'POST':
        # Get form data
        name = sanitize_string(request.form.get('name', ''), max_length=100)
        contact_number = sanitize_string(request.form.get('contact_number', ''), max_length=15)
        email = sanitize_string(request.form.get('email', ''), max_length=120)
        address = sanitize_string(request.form.get('address', ''))
        blood_group = request.form.get('blood_group', '')
        emergency_contact = sanitize_string(request.form.get('emergency_contact', ''), max_length=15)

        # Validation
        errors = []

        if not name:
            errors.append('Patient name is required.')
        if not contact_number:
            errors.append('Contact number is required.')

        # Validate email
        if email and not validate_email(email):
            errors.append('Please enter a valid email address.')

        # Validate phone
        if contact_number and not validate_phone(contact_number):
            errors.append('Please enter a valid 10-digit phone number.')

        # Check email uniqueness (excluding current patient)
        existing_email = User.query.filter_by(email=email).first()
        if existing_email and existing_email.id != patient.user_id:
            errors.append('Email already registered to another user.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('admin/edit_patient.html', patient=patient)

        # Update patient
        try:
            patient.name = name
            patient.contact_number = contact_number
            patient.address = address if address else None
            patient.blood_group = blood_group if blood_group else None
            patient.emergency_contact = emergency_contact if emergency_contact else None

            # Update user email
            patient.user.email = email

            db.session.commit()
            flash(f'Patient {name} updated successfully!', 'success')
            return redirect(url_for('admin.manage_patients'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error updating patient: {str(e)}', 'danger')

    # GET request
    return render_template('admin/edit_patient.html', patient=patient)


@admin_bp.route('/patients/toggle-active/<int:patient_id>', methods=['POST'])
@admin_required
def toggle_patient_active(patient_id):
    """
    Activate or deactivate (blacklist) a patient account
    """
    patient = Patient.query.get_or_404(patient_id)

    try:
        if patient.user.is_active:
            patient.user.deactivate()
            flash(f'Patient {patient.name} has been blacklisted.', 'warning')
        else:
            patient.user.activate()
            flash(f'Patient {patient.name} has been activated.', 'success')

    except Exception as e:
        flash(f'Error toggling patient status: {str(e)}', 'danger')

    return redirect(url_for('admin.manage_patients'))


# ==================== APPOINTMENT MANAGEMENT ====================

@admin_bp.route('/appointments')
@admin_required
def view_appointments():
    """
    View all appointments with filters
    """
    status_filter = request.args.get('status', '')
    date_filter = request.args.get('date', '')
    search_query = request.args.get('search', '').strip()

    query = Appointment.query

    # Apply filters
    if status_filter and status_filter in ['Booked', 'Completed', 'Cancelled']:
        query = query.filter_by(status=status_filter)

    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            query = query.filter_by(appointment_date=filter_date)
        except:
            pass

    if search_query:
        query = query.join(Patient).join(Doctor).filter(
            db.or_(
                Patient.name.ilike(f'%{search_query}%'),
                Doctor.name.ilike(f'%{search_query}%')
            )
        )

    appointments = query.order_by(
        Appointment.appointment_date.desc(),
        Appointment.appointment_time.desc()
    ).all()

    return render_template('admin/view_appointments.html',
                         appointments=appointments,
                         status_filter=status_filter,
                         date_filter=date_filter,
                         search_query=search_query)


@admin_bp.route('/appointments/view/<int:appointment_id>')
@admin_required
def view_appointment_details(appointment_id):
    """
    View detailed appointment information
    """
    appointment = Appointment.query.get_or_404(appointment_id)

    return render_template('admin/appointment_details.html',
                         appointment=appointment)


# ==================== SPECIALIZATION MANAGEMENT ====================

@admin_bp.route('/specializations')
@admin_required
def manage_specializations():
    """
    View and manage specializations
    """
    specializations = Specialization.get_all_specializations()

    return render_template('admin/manage_specializations.html',
                         specializations=specializations)


@admin_bp.route('/specializations/add', methods=['GET', 'POST'])
@admin_required
def add_specialization():
    """
    Add a new specialization
    """
    if request.method == 'POST':
        name = sanitize_string(request.form.get('name', ''), max_length=100)
        description = sanitize_string(request.form.get('description', ''))

        if not name:
            flash('Specialization name is required.', 'danger')
            return render_template('admin/add_specialization.html')

        # Check uniqueness
        if Specialization.query.filter_by(name=name).first():
            flash('Specialization already exists.', 'danger')
            return render_template('admin/add_specialization.html', form_data=request.form)

        try:
            specialization = Specialization(name=name, description=description)
            db.session.add(specialization)
            db.session.commit()

            flash(f'Specialization {name} added successfully!', 'success')
            return redirect(url_for('admin.manage_specializations'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error adding specialization: {str(e)}', 'danger')

    return render_template('admin/add_specialization.html')


# ==================== SEARCH ====================

@admin_bp.route('/search')
@admin_required
def search():
    """
    Global search for doctors, patients, appointments
    """
    query = request.args.get('q', '').strip()

    if not query:
        flash('Please enter a search term.', 'info')
        return redirect(url_for('admin.dashboard'))

    # Search doctors
    doctors = Doctor.search(query)

    # Search patients
    patients = Patient.search(query)

    # Search appointments
    appointments = Appointment.query.join(Patient).join(Doctor).filter(
        db.or_(
            Patient.name.ilike(f'%{query}%'),
            Doctor.name.ilike(f'%{query}%')
        )
    ).limit(20).all()

    return render_template('admin/search_results.html',
                         query=query,
                         doctors=doctors,
                         patients=patients,
                         appointments=appointments)
