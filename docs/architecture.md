# System Architecture Documentation

## Overview
The Hospital Management System follows the **Model-View-Controller (MVC)** architectural pattern with Flask as the web framework.

---

## Architecture Pattern: MVC

```
┌─────────────────────────────────────────────────────────┐
│                      USER BROWSER                        │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP Request
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   FLASK APPLICATION                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │              CONTROLLERS (Routes)                 │  │
│  │  - auth_controller.py                            │  │
│  │  - admin_controller.py                           │  │
│  │  - doctor_controller.py                          │  │
│  │  - patient_controller.py                         │  │
│  └──────────────┬───────────────────────┬───────────┘  │
│                 │                       │               │
│                 ▼                       ▼               │
│  ┌──────────────────────┐   ┌─────────────────────┐   │
│  │    MODELS (ORM)      │   │   VIEWS (Jinja2)   │   │
│  │  - User              │   │   - Templates       │   │
│  │  - Doctor            │   │   - HTML/CSS/JS     │   │
│  │  - Patient           │   │   - Bootstrap       │   │
│  │  - Appointment       │   └─────────────────────┘   │
│  │  - Treatment         │                              │
│  └──────────┬───────────┘                              │
│             │                                           │
└─────────────┼───────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────┐
│              SQLite Database (hospital.db)              │
└─────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Backend
- **Framework:** Flask 2.x
- **ORM:** Flask-SQLAlchemy
- **Database:** SQLite 3
- **Authentication:** Flask-Login
- **Password Hashing:** Flask-Bcrypt
- **Form Handling:** Flask-WTF
- **API (Optional):** Flask-RESTful

### Frontend
- **Template Engine:** Jinja2
- **CSS Framework:** Bootstrap 5
- **JavaScript:** Vanilla JS (Chart.js for graphs - optional)
- **HTML5 Form Validation**

### Development Tools
- **Python Version:** 3.8+
- **Virtual Environment:** venv
- **Package Manager:** pip

---

## Folder Structure Explanation

```
hospital_management_system/
│
├── app.py                      # Application entry point & configuration
├── config.py                   # Configuration classes (Dev, Prod)
├── requirements.txt            # Python dependencies
│
├── models/                     # DATABASE LAYER (ORM Models)
│   ├── __init__.py            # SQLAlchemy instance initialization
│   ├── user.py                # User authentication model
│   ├── admin.py               # Admin model
│   ├── doctor.py              # Doctor model
│   ├── patient.py             # Patient model
│   ├── appointment.py         # Appointment model
│   ├── treatment.py           # Treatment model
│   └── specialization.py      # Specialization model
│
├── controllers/                # CONTROLLER LAYER (Business Logic)
│   ├── __init__.py
│   ├── auth_controller.py     # Login, logout, register routes
│   ├── admin_controller.py    # Admin dashboard & operations
│   ├── doctor_controller.py   # Doctor dashboard & operations
│   └── patient_controller.py  # Patient dashboard & operations
│
├── api/                        # OPTIONAL REST API LAYER
│   ├── __init__.py
│   ├── doctor_api.py          # Doctor API resources
│   ├── patient_api.py         # Patient API resources
│   └── appointment_api.py     # Appointment API resources
│
├── templates/                  # VIEW LAYER (Jinja2 Templates)
│   ├── base.html              # Base template with navbar
│   ├── index.html             # Landing page
│   ├── login.html             # Login form
│   ├── register.html          # Registration form
│   │
│   ├── admin/                 # Admin templates
│   ├── doctor/                # Doctor templates
│   └── patient/               # Patient templates
│
├── static/                     # STATIC ASSETS
│   ├── css/
│   │   └── style.css          # Custom CSS
│   ├── js/
│   │   └── script.js          # Custom JavaScript
│   └── images/                # Images and icons
│
├── utils/                      # UTILITY LAYER
│   ├── __init__.py
│   ├── database.py            # DB initialization & seed data
│   ├── decorators.py          # Custom decorators (role checks)
│   └── helpers.py             # Helper functions
│
├── docs/                       # DOCUMENTATION
│   ├── database_schema.md     # Database documentation
│   ├── architecture.md        # This file
│   ├── api_documentation.md   # API endpoints (if implemented)
│   ├── setup_guide.md         # Installation instructions
│   ├── user_guide.md          # How to use the application
│   ├── changelog.md           # Version history
│   └── development_log.md     # Daily progress log
│
└── instance/
    └── hospital.db            # SQLite database file (auto-generated)
```

---

## Component Details

### 1. Application Entry Point (app.py)

**Responsibilities:**
- Initialize Flask application
- Configure database connection
- Register blueprints/controllers
- Set up Flask-Login
- Configure session management
- Run the application

**Key Code Structure:**
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)
login_manager = LoginManager(app)

# Register blueprints
from controllers import auth, admin, doctor, patient
app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(doctor)
app.register_blueprint(patient)

# Initialize database
from utils.database import init_db
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True)
```

---

### 2. Models Layer

**Purpose:** Define database schema using SQLAlchemy ORM

**Example Model Structure:**
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    admin = db.relationship('Admin', backref='user', uselist=False)
    doctor = db.relationship('Doctor', backref='user', uselist=False)
    patient = db.relationship('Patient', backref='user', uselist=False)
```

---

### 3. Controllers Layer

**Purpose:** Handle HTTP requests and business logic

**Blueprint Structure:**
```python
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@admin_required  # Custom decorator
def dashboard():
    # Business logic
    return render_template('admin/dashboard.html')
```

**Controller Responsibilities:**
- Route definition
- Request handling
- Form validation
- Database operations (via models)
- Response rendering

---

### 4. Views Layer (Templates)

**Purpose:** Render HTML using Jinja2 template engine

**Template Hierarchy:**
```
base.html                    # Navigation, footer, common elements
  ├── index.html            # Inherits from base
  ├── login.html            # Inherits from base
  └── admin/
      └── dashboard.html    # Inherits from base
```

**Jinja2 Features Used:**
- Template inheritance (`{% extends %}`)
- Block replacement (`{% block content %}`)
- Variables (`{{ variable }}`)
- Control structures (`{% if %}`, `{% for %}`)
- Filters (`{{ name|capitalize }}`)

---

### 5. Utilities Layer

**database.py:**
- Database initialization
- Create tables
- Seed default data (admin user, specializations)

**decorators.py:**
```python
from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
```

**helpers.py:**
- Common utility functions
- Date formatting
- Search algorithms
- Validation helpers

---

## Authentication Flow

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       │ Enters credentials
       ▼
┌────────────────────────────────┐
│  auth_controller.py (login)    │
│  1. Validate form data         │
│  2. Query User model           │
│  3. Check password hash        │
│  4. Verify is_active=True      │
└──────┬─────────────────────────┘
       │
       │ Success
       ▼
┌────────────────────────────────┐
│  Flask-Login                   │
│  1. Create session             │
│  2. Store user_id in session   │
│  3. Set current_user           │
└──────┬─────────────────────────┘
       │
       │ Check role
       ▼
┌────────────────────────────────┐
│  Redirect to Dashboard         │
│  - Admin → /admin/dashboard    │
│  - Doctor → /doctor/dashboard  │
│  - Patient → /patient/dashboard│
└────────────────────────────────┘
```

---

## Authorization Flow (Role-Based Access Control)

```python
@app.before_request
def check_user_active():
    if current_user.is_authenticated and not current_user.is_active:
        logout_user()
        flash('Your account has been deactivated.')
        return redirect(url_for('auth.login'))
```

**Decorator Usage:**
```python
@admin_required
def admin_only_route():
    pass

@doctor_required
def doctor_only_route():
    pass

@patient_required
def patient_only_route():
    pass
```

---

## Database Access Pattern

**Using SQLAlchemy ORM:**

```python
# CREATE
new_patient = Patient(name="John Doe", user_id=user.id)
db.session.add(new_patient)
db.session.commit()

# READ
patient = Patient.query.filter_by(id=patient_id).first()
all_patients = Patient.query.all()

# UPDATE
patient.contact_number = "1234567890"
db.session.commit()

# DELETE
db.session.delete(patient)
db.session.commit()
```

---

## Security Measures

1. **Password Security:**
   - Passwords hashed using bcrypt
   - Never store plain text passwords

2. **CSRF Protection:**
   - Flask-WTF provides CSRF tokens
   - All forms include CSRF tokens

3. **SQL Injection Prevention:**
   - Using SQLAlchemy ORM (parameterized queries)
   - No raw SQL queries

4. **Session Security:**
   - Flask secure sessions
   - Secret key configuration

5. **Input Validation:**
   - Frontend: HTML5 validation
   - Backend: WTForms validators

6. **Role-Based Access:**
   - Custom decorators
   - Route protection

---

## Scalability Considerations

**Current Design (MVP):**
- Single SQLite database
- Single server deployment
- Session-based authentication

**Future Enhancements:**
- Migrate to PostgreSQL/MySQL for production
- Implement caching (Redis)
- API-based architecture for mobile apps
- Microservices for different modules
- Load balancing for multiple servers

---

## Design Patterns Used

1. **MVC Pattern:** Separation of concerns
2. **Repository Pattern:** Database abstraction
3. **Decorator Pattern:** Role-based access control
4. **Factory Pattern:** Model creation
5. **Singleton Pattern:** Database connection

---

**Last Updated:** 2025-11-26
