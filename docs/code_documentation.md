# Code Documentation

Complete technical reference for all code in the Hospital Management System.

**Last Updated:** 2025-11-26
**Version:** 0.2.0
**Status:** Phase 2 Complete

---

## Table of Contents

1. [Application Core](#application-core)
2. [Configuration](#configuration)
3. [Database Models](#database-models)
4. [Utility Functions](#utility-functions)
5. [Code Examples](#code-examples)

---

## Application Core

### app.py

**Main application file with application factory pattern**

#### Functions

##### `create_app(config_name=None)`
Creates and configures the Flask application.

**Parameters:**
- `config_name` (str, optional): Configuration environment ('development', 'production', 'testing')

**Returns:**
- Flask app instance

**Functionality:**
- Loads configuration based on environment
- Initializes extensions (db, login_manager, bcrypt)
- Registers blueprints for different modules
- Creates database tables
- Seeds default data
- Sets up error handlers
- Configures template context processors

**Usage:**
```python
app = create_app('development')
app.run(debug=True)
```

#### Extension Instances

```python
db = SQLAlchemy()              # Database ORM
login_manager = LoginManager()  # Session management
bcrypt = Bcrypt()              # Password hashing
```

---

## Configuration

### config.py

**Configuration classes for different environments**

#### Class: `Config` (Base)
Base configuration with common settings.

**Attributes:**
- `SECRET_KEY`: Session encryption key
- `SQLALCHEMY_DATABASE_URI`: Database connection string
- `SQLALCHEMY_TRACK_MODIFICATIONS`: False (disable modification tracking)
- `PERMANENT_SESSION_LIFETIME`: 2 hours
- `SESSION_COOKIE_SECURE`: False (dev), True (prod)
- `SESSION_COOKIE_HTTPONLY`: True
- `WTF_CSRF_ENABLED`: True
- `ITEMS_PER_PAGE`: 10
- `MAX_CONTENT_LENGTH`: 5MB
- `UPLOAD_FOLDER`: static/uploads
- `APP_NAME`: 'Hospital Management System'
- `APP_VERSION`: '1.0.0'

#### Class: `DevelopmentConfig(Config)`
Development environment configuration.

**Attributes:**
- `DEBUG`: True
- `TESTING`: False

#### Class: `ProductionConfig(Config)`
Production environment configuration.

**Attributes:**
- `DEBUG`: False
- `SESSION_COOKIE_SECURE`: True (requires HTTPS)
- `SECRET_KEY`: Must be set via environment variable

#### Class: `TestingConfig(Config)`
Testing environment configuration.

**Attributes:**
- `TESTING`: True
- `SQLALCHEMY_DATABASE_URI`: 'sqlite:///:memory:' (in-memory database)
- `WTF_CSRF_ENABLED`: False (for testing)
- `BCRYPT_LOG_ROUNDS`: 4 (faster hashing for tests)

#### Function: `get_config(env=None)`
Get configuration based on environment.

**Parameters:**
- `env` (str, optional): Environment name

**Returns:**
- Configuration class

---

## Database Models

### models/user.py

#### Class: `User(UserMixin, db.Model)`
Base authentication model for all users.

**Table Name:** `users`

**Fields:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PRIMARY KEY, AUTOINCREMENT | Unique user identifier |
| username | String(80) | UNIQUE, NOT NULL, INDEX | Login username |
| email | String(120) | UNIQUE, NOT NULL, INDEX | Email address |
| password_hash | String(255) | NOT NULL | Hashed password |
| role | String(20) | NOT NULL, INDEX | User role (admin/doctor/patient) |
| is_active | Boolean | DEFAULT TRUE | Account status |
| created_at | DateTime | DEFAULT NOW | Account creation date |
| updated_at | DateTime | DEFAULT NOW, ON UPDATE | Last update date |

**Relationships:**
- `admin`: One-to-One with Admin model
- `doctor`: One-to-One with Doctor model
- `patient`: One-to-One with Patient model

**Methods:**

##### `__init__(username, email, password_hash, role)`
Initialize a new User.

##### `get_id()`
Return user ID as string (required by Flask-Login).

**Returns:** str

##### `is_admin()`
Check if user is admin.

**Returns:** bool

##### `is_doctor()`
Check if user is doctor.

**Returns:** bool

##### `is_patient()`
Check if user is patient.

**Returns:** bool

##### `to_dict()`
Convert user to dictionary for API responses.

**Returns:** dict

##### `@staticmethod validate_role(role)`
Validate user role.

**Parameters:**
- `role` (str): Role to validate

**Returns:** bool

##### `deactivate()`
Deactivate user account (blacklist).

##### `activate()`
Activate user account.

**Example:**
```python
user = User(username='john', email='john@example.com',
            password_hash=hashed_password, role='patient')
db.session.add(user)
db.session.commit()

if user.is_patient():
    print("User is a patient")
```

---

### models/admin.py

#### Class: `Admin(db.Model)`
Hospital administrative staff model.

**Table Name:** `admins`

**Fields:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PRIMARY KEY, AUTOINCREMENT | Unique admin identifier |
| user_id | Integer | FOREIGN KEY (users.id), UNIQUE | Link to User |
| name | String(100) | NOT NULL | Admin full name |
| contact_number | String(15) | NULLABLE | Contact number |

**Relationships:**
- `user`: Backref to User model

**Methods:**

##### `__init__(user_id, name, contact_number=None)`
Initialize a new Admin.

##### `to_dict()`
Convert admin to dictionary.

**Returns:** dict

##### `@staticmethod get_by_user_id(user_id)`
Get admin by user ID.

**Returns:** Admin or None

##### `@staticmethod get_all_admins()`
Get all admins.

**Returns:** List[Admin]

---

### models/specialization.py

#### Class: `Specialization(db.Model)`
Medical specializations/departments model.

**Table Name:** `specializations`

**Fields:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PRIMARY KEY, AUTOINCREMENT | Unique specialization ID |
| name | String(100) | UNIQUE, NOT NULL, INDEX | Specialization name |
| description | Text | NULLABLE | Description |

**Relationships:**
- `doctors`: One-to-Many with Doctor model

**Properties:**

##### `doctor_count`
Get count of doctors in this specialization.

**Returns:** int

**Methods:**

##### `__init__(name, description=None)`
Initialize a new Specialization.

##### `to_dict()`
Convert specialization to dictionary.

**Returns:** dict

##### `@staticmethod get_all_specializations()`
Get all specializations ordered by name.

**Returns:** List[Specialization]

##### `@staticmethod get_by_name(name)`
Get specialization by name.

**Returns:** Specialization or None

##### `@staticmethod search(query)`
Search specializations by name.

**Returns:** List[Specialization]

---

### models/doctor.py

#### Class: `Doctor(db.Model)`
Medical professionals model.

**Table Name:** `doctors`

**Fields:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PRIMARY KEY, AUTOINCREMENT | Unique doctor identifier |
| user_id | Integer | FOREIGN KEY (users.id), UNIQUE | Link to User |
| specialization_id | Integer | FOREIGN KEY (specializations.id) | Specialization |
| name | String(100) | NOT NULL, INDEX | Doctor full name |
| qualification | String(200) | NULLABLE | Degrees and certifications |
| experience_years | Integer | NULLABLE | Years of experience |
| contact_number | String(15) | NULLABLE | Contact number |
| profile_image | String(255) | NULLABLE | Profile picture path |

**Relationships:**
- `user`: Backref to User model
- `specialization`: Backref to Specialization model
- `appointments`: One-to-Many with Appointment model
- `availability_slots`: One-to-Many with DoctorAvailability model

**Properties:**

##### `total_appointments`
Get total number of appointments.

**Returns:** int

##### `upcoming_appointments`
Get upcoming appointments (today onwards, status=Booked).

**Returns:** List[Appointment]

**Methods:**

##### `__init__(user_id, name, specialization_id, qualification=None, experience_years=None, contact_number=None)`
Initialize a new Doctor.

##### `get_availability_for_next_7_days()`
Get availability slots for next 7 days.

**Returns:** List[DoctorAvailability]

##### `is_available_on(check_date, check_time)`
Check if doctor is available on specific date and time.

**Parameters:**
- `check_date` (date): Date to check
- `check_time` (time): Time to check

**Returns:** bool

##### `to_dict(include_availability=False)`
Convert doctor to dictionary.

**Parameters:**
- `include_availability` (bool): Include availability data

**Returns:** dict

##### `@staticmethod get_by_user_id(user_id)`
Get doctor by user ID.

**Returns:** Doctor or None

##### `@staticmethod get_by_specialization(specialization_id)`
Get all doctors by specialization.

**Returns:** List[Doctor]

##### `@staticmethod search(query)`
Search doctors by name.

**Returns:** List[Doctor]

##### `@staticmethod get_all_doctors()`
Get all doctors ordered by name.

**Returns:** List[Doctor]

**Example:**
```python
doctor = Doctor(user_id=user.id, name='Dr. Smith',
                specialization_id=1, qualification='MD, DM')
db.session.add(doctor)
db.session.commit()

# Check availability
if doctor.is_available_on(date(2025, 11, 26), time(10, 0)):
    print("Doctor is available")
```

---

#### Class: `DoctorAvailability(db.Model)`
Doctor availability scheduling (7-day rolling window).

**Table Name:** `doctor_availability`

**Fields:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PRIMARY KEY, AUTOINCREMENT | Unique availability ID |
| doctor_id | Integer | FOREIGN KEY (doctors.id) | Link to Doctor |
| available_date | Date | NOT NULL, INDEX | Available date |
| start_time | Time | NOT NULL | Availability start time |
| end_time | Time | NOT NULL | Availability end time |
| is_available | Boolean | DEFAULT TRUE | Availability status |

**Indexes:**
- Composite index on (doctor_id, available_date)

**Methods:**

##### `__init__(doctor_id, available_date, start_time, end_time, is_available=True)`
Initialize a new availability slot.

##### `to_dict()`
Convert availability to dictionary.

**Returns:** dict

##### `@staticmethod set_doctor_availability(doctor_id, available_date, start_time, end_time)`
Set or update doctor availability for a specific date.

##### `@staticmethod remove_past_availability()`
Remove availability slots for dates before today.

---

### models/patient.py

#### Class: `Patient(db.Model)`
Patients seeking medical care model.

**Table Name:** `patients`

**Fields:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PRIMARY KEY, AUTOINCREMENT | Unique patient identifier |
| user_id | Integer | FOREIGN KEY (users.id), UNIQUE | Link to User |
| name | String(100) | NOT NULL, INDEX | Patient full name |
| date_of_birth | Date | NULLABLE | Date of birth |
| gender | String(10) | NULLABLE | Gender (Male/Female/Other) |
| contact_number | String(15) | NOT NULL | Contact number |
| address | Text | NULLABLE | Residential address |
| blood_group | String(5) | NULLABLE | Blood group (A+, B-, etc.) |
| emergency_contact | String(15) | NULLABLE | Emergency contact number |

**Relationships:**
- `user`: Backref to User model
- `appointments`: One-to-Many with Appointment model

**Properties:**

##### `age`
Calculate patient age from date of birth.

**Returns:** int or None

##### `total_appointments`
Get total number of appointments.

**Returns:** int

##### `upcoming_appointments`
Get upcoming appointments (status=Booked, date >= today).

**Returns:** List[Appointment]

##### `past_appointments`
Get past appointments (status=Completed/Cancelled or date < today).

**Returns:** List[Appointment]

**Methods:**

##### `__init__(user_id, name, contact_number, date_of_birth=None, gender=None, address=None, blood_group=None, emergency_contact=None)`
Initialize a new Patient.

##### `get_treatment_history()`
Get complete treatment history.

**Returns:** List[dict] with treatment details

##### `to_dict(include_appointments=False)`
Convert patient to dictionary.

**Parameters:**
- `include_appointments` (bool): Include appointment data

**Returns:** dict

##### `@staticmethod get_by_user_id(user_id)`
Get patient by user ID.

**Returns:** Patient or None

##### `@staticmethod search(query)`
Search patients by name or contact number.

**Returns:** List[Patient]

##### `@staticmethod get_all_patients()`
Get all patients ordered by name.

**Returns:** List[Patient]

##### `@staticmethod validate_blood_group(blood_group)`
Validate blood group format.

**Returns:** bool

##### `@staticmethod validate_gender(gender)`
Validate gender value.

**Returns:** bool

**Example:**
```python
patient = Patient(user_id=user.id, name='John Doe',
                  contact_number='1234567890',
                  date_of_birth=date(1990, 1, 1),
                  gender='Male', blood_group='O+')
db.session.add(patient)
db.session.commit()

print(f"Patient age: {patient.age} years")
```

---

### models/appointment.py

#### Class: `Appointment(db.Model)`
Scheduled appointments between patients and doctors.

**Table Name:** `appointments`

**Fields:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PRIMARY KEY, AUTOINCREMENT | Unique appointment ID |
| patient_id | Integer | FOREIGN KEY (patients.id), INDEX | Link to Patient |
| doctor_id | Integer | FOREIGN KEY (doctors.id), INDEX | Link to Doctor |
| appointment_date | Date | NOT NULL, INDEX | Appointment date |
| appointment_time | Time | NOT NULL | Appointment time |
| status | String(20) | DEFAULT 'Booked', INDEX | Status (Booked/Completed/Cancelled) |
| booking_date | DateTime | DEFAULT NOW | When booking was made |
| updated_at | DateTime | DEFAULT NOW, ON UPDATE | Last update |
| cancellation_reason | Text | NULLABLE | Reason if cancelled |

**Relationships:**
- `patient`: Backref to Patient model
- `doctor`: Backref to Doctor model
- `treatment`: One-to-One with Treatment model

**Indexes:**
- Composite index on (doctor_id, appointment_date, appointment_time)

**Properties:**

##### `is_upcoming`
Check if appointment is in the future.

**Returns:** bool

##### `is_past`
Check if appointment is in the past.

**Returns:** bool

**Methods:**

##### `__init__(patient_id, doctor_id, appointment_date, appointment_time, status='Booked')`
Initialize a new Appointment.

##### `mark_completed()`
Mark appointment as completed.

##### `mark_cancelled(reason=None)`
Mark appointment as cancelled.

**Parameters:**
- `reason` (str, optional): Cancellation reason

##### `can_be_cancelled()`
Check if appointment can be cancelled.

**Returns:** bool

##### `can_be_completed()`
Check if appointment can be marked as completed.

**Returns:** bool

##### `to_dict(include_treatment=False)`
Convert appointment to dictionary.

**Parameters:**
- `include_treatment` (bool): Include treatment data

**Returns:** dict

##### `@staticmethod check_double_booking(doctor_id, appointment_date, appointment_time)`
Check if doctor already has an appointment at the same date/time.

**Parameters:**
- `doctor_id` (int): Doctor ID
- `appointment_date` (date): Appointment date
- `appointment_time` (time): Appointment time

**Returns:** bool (True if available, False if booked)

##### `@staticmethod create_appointment(patient_id, doctor_id, appointment_date, appointment_time)`
Create a new appointment with double-booking check.

**Returns:** (success: bool, message: str, appointment: Appointment or None)

##### `@staticmethod get_appointments_by_doctor(doctor_id, status=None, from_date=None)`
Get appointments for a specific doctor.

**Returns:** List[Appointment]

##### `@staticmethod get_appointments_by_patient(patient_id, status=None)`
Get appointments for a specific patient.

**Returns:** List[Appointment]

##### `@staticmethod get_all_appointments(status=None, from_date=None, to_date=None)`
Get all appointments with optional filters.

**Returns:** List[Appointment]

##### `@staticmethod get_today_appointments(doctor_id=None)`
Get appointments for today.

**Returns:** List[Appointment]

##### `@staticmethod get_upcoming_appointments(days=7, doctor_id=None)`
Get upcoming appointments for next N days.

**Returns:** List[Appointment]

##### `@staticmethod validate_status(status)`
Validate appointment status.

**Returns:** bool

**Example:**
```python
# Book appointment with double-booking check
success, message, apt = Appointment.create_appointment(
    patient_id=1, doctor_id=2,
    appointment_date=date(2025, 11, 27),
    appointment_time=time(10, 0)
)

if success:
    print(f"Appointment booked: {apt.id}")
else:
    print(f"Error: {message}")
```

---

### models/treatment.py

#### Class: `Treatment(db.Model)`
Medical treatment records for completed appointments.

**Table Name:** `treatments`

**Fields:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PRIMARY KEY, AUTOINCREMENT | Unique treatment ID |
| appointment_id | Integer | FOREIGN KEY (appointments.id), UNIQUE | Link to Appointment (1:1) |
| diagnosis | Text | NOT NULL | Medical diagnosis |
| prescription | Text | NULLABLE | Prescribed medications |
| notes | Text | NULLABLE | Doctor's notes |
| treatment_date | DateTime | DEFAULT NOW | Treatment creation date |
| updated_at | DateTime | DEFAULT NOW, ON UPDATE | Last update |

**Relationships:**
- `appointment`: Backref to Appointment model (One-to-One)

**Methods:**

##### `__init__(appointment_id, diagnosis, prescription=None, notes=None)`
Initialize a new Treatment record.

##### `to_dict()`
Convert treatment to dictionary.

**Returns:** dict

##### `update_treatment(diagnosis=None, prescription=None, notes=None)`
Update treatment details.

##### `@staticmethod create_treatment(appointment_id, diagnosis, prescription=None, notes=None)`
Create a new treatment record and mark appointment as completed.

**Returns:** (success: bool, message: str, treatment: Treatment or None)

##### `@staticmethod get_treatment_by_appointment(appointment_id)`
Get treatment record by appointment ID.

**Returns:** Treatment or None

##### `@staticmethod get_patient_treatment_history(patient_id)`
Get all treatment records for a patient.

**Returns:** List[Treatment]

##### `@staticmethod get_doctor_treatments(doctor_id)`
Get all treatments provided by a doctor.

**Returns:** List[Treatment]

##### `@staticmethod search_by_diagnosis(query)`
Search treatments by diagnosis.

**Returns:** List[Treatment]

**Example:**
```python
# Create treatment and complete appointment
success, message, treatment = Treatment.create_treatment(
    appointment_id=1,
    diagnosis='Hypertension',
    prescription='Amlodipine 5mg, OD for 30 days',
    notes='Follow up in 2 weeks'
)

if success:
    print("Treatment recorded successfully")
```

---

## Utility Functions

### utils/database.py

Database initialization and management utilities.

#### Functions

##### `init_db()`
Initialize database with default data.
- Creates default admin user
- Creates default specializations
- Should be called after db.create_all()

##### `create_default_admin()`
Create default admin user programmatically.

**Credentials:**
- Username: admin
- Password: admin123
- Email: admin@hospital.com

**Returns:** User or None

##### `create_default_specializations()`
Create 10 default medical specializations.

**Specializations:**
1. General Medicine
2. Cardiology
3. Neurology
4. Orthopedics
5. Pediatrics
6. Dermatology
7. ENT
8. Psychiatry
9. Gynecology
10. Ophthalmology

##### `reset_database()`
⚠️ DANGER: Drop all tables and recreate them.
Use only in development!

##### `cleanup_old_data()`
Clean up old data (past availability slots, etc.)

##### `get_database_stats()`
Get database statistics.

**Returns:** dict with counts of various entities

##### `print_database_stats()`
Print database statistics to console.

##### `verify_admin_exists()`
Verify that default admin user exists.

**Returns:** bool

##### `create_backup()`
Create database backup with timestamp.

**Returns:** bool

---

### utils/decorators.py

Role-based access control decorators.

#### Decorators

##### `@admin_required`
Restrict access to admin users only.

**Usage:**
```python
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')
```

##### `@doctor_required`
Restrict access to doctor users only.

##### `@patient_required`
Restrict access to patient users only.

##### `@role_required(*roles)`
Flexible role checking for multiple roles.

**Usage:**
```python
@app.route('/appointments')
@role_required('doctor', 'patient')
def appointments():
    return render_template('appointments.html')
```

##### `@anonymous_required`
Restrict access to non-logged-in users (for login/register pages).

##### `@check_account_active`
Check if user account is active.

##### `@validate_ownership(model, id_param='id', owner_field='user_id')`
Validate that current user owns the resource.

##### `@ajax_required`
Ensure request is AJAX.

##### `@rate_limit(max_requests=10, window=60)`
Simple rate limiting.

---

### utils/helpers.py

Common helper functions (30+ functions).

#### Date/Time Functions

##### `format_date(date_obj, format_string='%Y-%m-%d')`
Format date object to string.

**Returns:** str or None

##### `format_time(time_obj, format_string='%H:%M')`
Format time object to string.

**Returns:** str or None

##### `format_datetime(datetime_obj, format_string='%Y-%m-%d %H:%M:%S')`
Format datetime object to string.

**Returns:** str or None

##### `parse_date(date_string, format_string='%Y-%m-%d')`
Parse date string to date object.

**Returns:** date or None

##### `parse_time(time_string, format_string='%H:%M')`
Parse time string to time object.

**Returns:** time or None

##### `calculate_age(birth_date)`
Calculate age from date of birth.

**Parameters:**
- `birth_date` (date or str): Date of birth

**Returns:** int (age in years) or None

**Example:**
```python
age = calculate_age(date(1990, 1, 1))
print(f"Age: {age} years")
```

##### `get_date_range(start_date, end_date)`
Get list of dates between start and end date.

**Returns:** List[date]

##### `get_next_n_days(n=7, start_date=None)`
Get next N days from start date.

**Returns:** List[date]

##### `is_weekend(check_date)`
Check if date is weekend.

**Returns:** bool

##### `get_weekday_name(check_date)`
Get weekday name from date.

**Returns:** str (e.g., 'Monday')

##### `generate_time_slots(start_time, end_time, interval_minutes=30)`
Generate time slots between start and end time.

**Returns:** List[time]

**Example:**
```python
slots = generate_time_slots(time(9, 0), time(17, 0), 30)
# Returns: [09:00, 09:30, 10:00, ..., 17:00]
```

##### `is_past_datetime(check_date, check_time=None)`
Check if date/time is in the past.

**Returns:** bool

##### `get_current_time()`
Get current time.

**Returns:** time

##### `get_today()`
Get today's date.

**Returns:** date

#### Validation Functions

##### `validate_email(email)`
Validate email address format.

**Returns:** bool

##### `validate_phone(phone)`
Validate phone number format (10 digits).

**Returns:** bool

**Example:**
```python
if validate_email('user@example.com'):
    print("Valid email")

if validate_phone('1234567890'):
    print("Valid phone")
```

#### String Functions

##### `sanitize_string(input_string, max_length=None)`
Sanitize user input string.

**Returns:** str

##### `truncate_string(text, length=50, suffix='...')`
Truncate string to specified length.

**Returns:** str

##### `format_phone(phone)`
Format phone number to standard format (XXX-XXX-XXXX).

**Returns:** str

#### UI Helper Functions

##### `get_status_badge_class(status)`
Get Bootstrap badge class for appointment status.

**Parameters:**
- `status` (str): Appointment status

**Returns:** str (Bootstrap class name)

**Example:**
```python
badge_class = get_status_badge_class('Booked')
# Returns: 'badge-primary'
```

##### `paginate_list(items, page=1, per_page=10)`
Paginate a list of items.

**Returns:** dict with pagination info

**Example:**
```python
result = paginate_list(items, page=1, per_page=10)
# Returns: {
#   'items': [...],
#   'page': 1,
#   'per_page': 10,
#   'total_items': 50,
#   'total_pages': 5,
#   'has_prev': False,
#   'has_next': True
# }
```

##### `flash_form_errors(form)`
Flash all form validation errors.

##### `allowed_file(filename, allowed_extensions=None)`
Check if file has allowed extension.

**Returns:** bool

---

## Code Examples

### Creating a New User

```python
from app import db, bcrypt
from models.user import User
from models.patient import Patient

# Hash password
password_hash = bcrypt.generate_password_hash('password123').decode('utf-8')

# Create user
user = User(
    username='john_doe',
    email='john@example.com',
    password_hash=password_hash,
    role='patient'
)
db.session.add(user)
db.session.flush()  # Get user.id

# Create patient profile
patient = Patient(
    user_id=user.id,
    name='John Doe',
    contact_number='1234567890',
    date_of_birth=date(1990, 1, 1),
    gender='Male',
    blood_group='O+'
)
db.session.add(patient)
db.session.commit()
```

### Booking an Appointment

```python
from models.appointment import Appointment
from datetime import date, time

# Book with double-booking check
success, message, appointment = Appointment.create_appointment(
    patient_id=1,
    doctor_id=2,
    appointment_date=date(2025, 11, 27),
    appointment_time=time(10, 0)
)

if success:
    print(f"Appointment booked successfully! ID: {appointment.id}")
else:
    print(f"Error: {message}")
```

### Completing an Appointment with Treatment

```python
from models.treatment import Treatment

# Create treatment and mark appointment complete
success, message, treatment = Treatment.create_treatment(
    appointment_id=1,
    diagnosis='Common cold',
    prescription='Paracetamol 500mg, TID for 3 days',
    notes='Rest and drink plenty of fluids'
)

if success:
    print("Treatment recorded and appointment completed!")
else:
    print(f"Error: {message}")
```

### Searching for Doctors

```python
from models.doctor import Doctor
from models.specialization import Specialization

# Get all doctors in Cardiology
cardiology = Specialization.get_by_name('Cardiology')
doctors = Doctor.get_by_specialization(cardiology.id)

# Search doctors by name
doctors = Doctor.search('smith')

# Get doctor's availability
doctor = Doctor.query.get(1)
availability = doctor.get_availability_for_next_7_days()
```

### Getting Patient Treatment History

```python
from models.patient import Patient

patient = Patient.query.get(1)
history = patient.get_treatment_history()

for record in history:
    print(f"Date: {record['appointment_date']}")
    print(f"Doctor: {record['doctor_name']}")
    print(f"Diagnosis: {record['diagnosis']}")
    print(f"Prescription: {record['prescription']}")
    print("---")
```

### Using Decorators

```python
from flask import Blueprint
from utils.decorators import admin_required, doctor_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    # Only admins can access this
    return render_template('admin/dashboard.html')

@admin_bp.route('/doctors')
@admin_required
def manage_doctors():
    # Only admins can access this
    doctors = Doctor.get_all_doctors()
    return render_template('admin/doctors.html', doctors=doctors)
```

### Using Helper Functions

```python
from utils.helpers import (
    calculate_age, format_date, validate_email,
    generate_time_slots, get_next_n_days
)

# Calculate age
age = calculate_age(date(1990, 1, 1))  # Returns: 35

# Format date
formatted = format_date(date.today())  # Returns: '2025-11-26'

# Validate email
is_valid = validate_email('user@example.com')  # Returns: True

# Generate time slots
slots = generate_time_slots(time(9, 0), time(17, 0), 30)
# Returns: [09:00, 09:30, 10:00, ..., 17:00]

# Get next 7 days
dates = get_next_n_days(7)
# Returns: [today, tomorrow, ..., 7 days from now]
```

---

## Database Queries Examples

### Complex Queries

```python
from models.appointment import Appointment
from models.doctor import Doctor
from datetime import date, timedelta

# Get all booked appointments for next week
today = date.today()
next_week = today + timedelta(days=7)

appointments = Appointment.query.filter(
    Appointment.appointment_date >= today,
    Appointment.appointment_date <= next_week,
    Appointment.status == 'Booked'
).join(Doctor).order_by(
    Appointment.appointment_date,
    Appointment.appointment_time
).all()

# Get doctor's completed appointments with treatments
from models.treatment import Treatment

completed = Appointment.query.filter_by(
    doctor_id=1,
    status='Completed'
).join(Treatment).all()

# Search patients by multiple criteria
from models.patient import Patient

patients = Patient.query.filter(
    db.or_(
        Patient.name.ilike('%john%'),
        Patient.contact_number.ilike('%1234%')
    )
).all()
```

---

## Error Handling Examples

```python
from sqlalchemy.exc import IntegrityError

try:
    # Create appointment
    appointment = Appointment(
        patient_id=1,
        doctor_id=2,
        appointment_date=date(2025, 11, 27),
        appointment_time=time(10, 0)
    )
    db.session.add(appointment)
    db.session.commit()

except IntegrityError as e:
    db.session.rollback()
    print("Error: Duplicate appointment or invalid foreign key")

except Exception as e:
    db.session.rollback()
    print(f"Unexpected error: {str(e)}")
```

---

## Summary Statistics

**Total Models:** 8 (7 + 1 sub-model)
**Total Utility Functions:** 40+
**Total Decorators:** 7
**Total Lines of Code:** ~2,500
**Database Tables:** 9
**Default Specializations:** 10

---

**End of Code Documentation**
**For user guides, see:** user_guide.md
**For setup instructions, see:** setup_guide.md
**For API reference, see:** api_documentation.md
