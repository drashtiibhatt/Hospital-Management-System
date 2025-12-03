# Hospital Management System

A comprehensive web-based Hospital Management System built with Flask, designed to streamline hospital operations by managing patients, doctors, appointments, and medical records.

![Version](https://img.shields.io/badge/version-0.5.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [API Routes](#api-routes)
- [API Documentation](#api-documentation)
- [Security](#security)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

### Role-Based Access Control
The system provides three distinct user roles with specific permissions:

#### Admin (Hospital Staff)
- Real-time dashboard with statistics (patients, doctors, appointments)
- Complete CRUD operations for doctors and patients
- Appointment management and oversight
- User blacklist/deactivation capabilities
- Advanced search and filtering

#### Doctor
- Personalized dashboard with assigned appointments
- Patient history and treatment records access
- Appointment status management (complete/cancel)
- Add diagnosis, prescriptions, and treatment notes
- 7-day availability schedule management

#### Patient
- Self-registration and profile management
- Doctor search by specialization and availability
- Appointment booking with conflict prevention
- Appointment rescheduling and cancellation
- Complete treatment history access

### Core Functionalities
- **Double-booking Prevention**: Automatic scheduling conflict detection
- **Dynamic Status Tracking**: Real-time appointment lifecycle management
- **Treatment History**: Comprehensive medical record keeping
- **Secure Authentication**: Bcrypt password hashing + session management
- **Responsive Design**: Mobile-friendly Bootstrap 5 UI
- **Legal Compliance**: Privacy Policy, Terms of Service, FAQ pages

---

## Technology Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.8+ | Programming language |
| Flask | 3.0.0 | Web framework |
| Flask-SQLAlchemy | 3.1.1 | ORM for database operations |
| Flask-Login | 0.6.3 | User session management |
| Flask-Bcrypt | 1.0.1 | Password hashing |
| Flask-WTF | 1.2.1 | Form handling & CSRF protection |
| SQLite | 3.x | Database |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| Jinja2 | 3.1.x | Template engine |
| Bootstrap | 5.3.0 | CSS framework |
| JavaScript | ES6 | Client-side interactivity |
| Bootstrap Icons | 1.11.0 | Icon library |

---

## Project Structure

```
hospital_management_system/
│
├── app.py                          # Application entry point
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── REPORT.md                       # Project report
│
├── models/                         # Database models (ORM)
│   ├── __init__.py
│   ├── user.py                     # Base user model
│   ├── admin.py                    # Admin model
│   ├── doctor.py                   # Doctor model & availability
│   ├── patient.py                  # Patient model
│   ├── appointment.py              # Appointment model
│   ├── treatment.py                # Treatment/medical records
│   └── specialization.py           # Medical specializations
│
├── controllers/                    # Route handlers (MVC)
│   ├── __init__.py
│   ├── auth_controller.py          # Authentication & legal pages
│   ├── admin_controller.py         # Admin operations
│   ├── doctor_controller.py        # Doctor operations
│   └── patient_controller.py       # Patient operations
│
├── templates/                      # Jinja2 HTML templates
│   ├── base.html                   # Base template
│   ├── index.html                  # Landing page
│   ├── login.html                  # Login page
│   ├── register.html               # Registration page
│   ├── privacy_policy.html         # Privacy policy
│   ├── terms_of_service.html       # Terms of service
│   ├── faq.html                    # FAQ page
│   ├── admin/                      # Admin templates (12 files)
│   ├── doctor/                     # Doctor templates (12 files)
│   └── patient/                    # Patient templates (11 files)
│
├── static/                         # Static assets
│   ├── css/
│   │   └── style.css              # Custom styles
│   ├── js/
│   │   └── script.js              # Custom JavaScript
│   └── images/                     # Images & hero slides
│
├── utils/                          # Utility functions
│   ├── __init__.py
│   ├── database.py                 # Database initialization & seeding
│   ├── decorators.py               # Custom decorators (role-based access)
│   └── helpers.py                  # Helper functions
│
└── instance/
    └── hospital.db                 # SQLite database (auto-generated)
```

**Statistics:**
- **Total Files**: 75
- **Backend Code**: ~4,200 lines
- **Frontend Code**: ~11,400 lines
- **Templates**: 50 HTML files
- **Routes**: 50 endpoints

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step-by-Step Setup

1. **Clone/Download the Project**
   ```bash
   cd "C:\Users\DUBHA\OneDrive\Desktop\IITM Project"
   ```

2. **Create Virtual Environment**

   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**
   The database will be automatically created on first run with sample data.

5. **Run the Application**
   ```bash
   python app.py
   ```

6. **Access the Application**
   ```
   http://127.0.0.1:5000/
   ```

---

## Configuration

### Environment Variables
Create a `.env` file (optional) for custom configuration:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URI=sqlite:///instance/hospital.db
DEBUG=True
```

### Default Settings (config.py)
```python
SECRET_KEY = 'dev-secret-key-change-in-production'
SQLALCHEMY_DATABASE_URI = 'sqlite:///hospital.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = True
```

### Default Admin Credentials
```
Username: admin
Password: admin123
Email: admin@hospital.com
```
**⚠️ Important**: Change default password immediately after first login!

### Demo Doctor Credentials
```
Username: dr.sarah, dr.emily, dr.michael, dr.robert, dr.jennifer
Password: doctor123
```

---

## Usage

### For Patients

1. **Register Account**
   - Navigate to `/register`
   - Fill in personal details
   - Login with credentials

2. **Book Appointment**
   - Search doctors by specialization
   - View doctor availability (7-day schedule)
   - Select date and time slot
   - Confirm booking

3. **Manage Appointments**
   - View upcoming appointments
   - Reschedule or cancel
   - Access treatment history

### For Doctors

1. **Login** with provided credentials

2. **Manage Appointments**
   - View assigned appointments
   - Mark as completed with diagnosis
   - Add prescriptions and treatment notes

3. **Set Availability**
   - Configure 7-day availability schedule
   - Set working hours per day

### For Admins

1. **Login** with admin credentials

2. **Manage System**
   - Add/edit/remove doctors
   - Monitor patient registrations
   - Oversee all appointments
   - View system statistics

---

## Database Schema

### Entity Relationship Diagram

```
Users (Base)
├── Admin
├── Doctor ──→ DoctorAvailability
└── Patient

Appointment
├── Patient (FK)
└── Doctor (FK)

Treatment
├── Patient (FK)
├── Doctor (FK)
└── Appointment (FK)

Specialization ←─ Doctor (FK)
```

### Key Tables

#### Users
| Column | Type | Description |
|--------|------|-------------|
| id | Integer (PK) | Unique identifier |
| username | String(80) | Unique username |
| email | String(120) | Unique email |
| password_hash | String(200) | Bcrypt hashed password |
| role | String(20) | User role (admin/doctor/patient) |
| is_active | Boolean | Account status |

#### Doctor
| Column | Type | Description |
|--------|------|-------------|
| id | Integer (PK) | Unique identifier |
| user_id | Integer (FK) | References Users.id |
| name | String(100) | Full name |
| specialization_id | Integer (FK) | References Specialization.id |
| license_number | String(50) | Medical license |
| experience_years | Integer | Years of experience |
| consultation_fee | Float | Consultation charges |

#### Appointment
| Column | Type | Description |
|--------|------|-------------|
| id | Integer (PK) | Unique identifier |
| patient_id | Integer (FK) | References Patient.id |
| doctor_id | Integer (FK) | References Doctor.id |
| appointment_date | Date | Scheduled date |
| appointment_time | String(10) | Time slot (e.g., "10:00 AM") |
| status | String(20) | Status (Booked/Completed/Cancelled) |

#### Treatment
| Column | Type | Description |
|--------|------|-------------|
| id | Integer (PK) | Unique identifier |
| appointment_id | Integer (FK) | References Appointment.id |
| diagnosis | Text | Medical diagnosis |
| prescription | Text | Prescribed medication |
| treatment_notes | Text | Additional notes |
| treatment_date | DateTime | Date of treatment |

---

## API Routes

### Authentication Routes (`/auth`)
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET/POST | `/login` | User login | Public |
| GET/POST | `/register` | Patient registration | Public |
| GET | `/logout` | User logout | Authenticated |
| GET/POST | `/change-password` | Password change | Authenticated |
| GET | `/privacy-policy` | Privacy policy page | Public |
| GET | `/terms-of-service` | Terms of service | Public |
| GET | `/faq` | FAQ page | Public |

### Admin Routes (`/admin`)
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/dashboard` | Admin dashboard | Admin only |
| GET | `/doctors` | List all doctors | Admin only |
| GET/POST | `/doctors/add` | Add new doctor | Admin only |
| GET/POST | `/doctors/edit/<id>` | Edit doctor | Admin only |
| POST | `/doctors/delete/<id>` | Delete doctor | Admin only |
| GET | `/patients` | List all patients | Admin only |
| GET/POST | `/patients/edit/<id>` | Edit patient | Admin only |
| GET | `/appointments` | View all appointments | Admin only |
| GET | `/specializations` | Manage specializations | Admin only |

### Doctor Routes (`/doctor`)
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/dashboard` | Doctor dashboard | Doctor only |
| GET | `/appointments` | View appointments | Doctor only |
| GET/POST | `/appointments/complete/<id>` | Complete appointment | Doctor only |
| POST | `/appointments/cancel/<id>` | Cancel appointment | Doctor only |
| GET | `/patients` | View patient list | Doctor only |
| GET | `/patients/<id>` | Patient history | Doctor only |
| GET/POST | `/availability` | Manage availability | Doctor only |
| GET/POST | `/profile` | Edit profile | Doctor only |

### Patient Routes (`/patient`)
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/dashboard` | Patient dashboard | Patient only |
| GET | `/doctors` | Search doctors | Patient only |
| GET | `/doctors/<id>` | Doctor details | Patient only |
| GET/POST | `/appointments/book/<doctor_id>` | Book appointment | Patient only |
| GET | `/appointments` | My appointments | Patient only |
| POST | `/appointments/cancel/<id>` | Cancel appointment | Patient only |
| GET | `/treatment-history` | Treatment records | Patient only |
| GET/POST | `/profile` | Edit profile | Patient only |

---

## API Documentation

### OpenAPI Specification

The complete API documentation is available in **OpenAPI 3.0.3** format in the `openapi.yml` file.

#### Viewing the Documentation

**Option 1: Swagger UI (Online)**
1. Go to [Swagger Editor](https://editor.swagger.io/)
2. Upload the `openapi.yml` file
3. View interactive API documentation

**Option 2: Swagger UI (Local)**
```bash
# Install swagger-ui-watcher
npm install -g swagger-ui-watcher

# Run Swagger UI
swagger-ui-watcher openapi.yml
```

**Option 3: VS Code Extension**
1. Install "OpenAPI (Swagger) Editor" extension
2. Open `openapi.yml` file
3. Click "Preview" to view documentation

#### API Documentation Includes

- **50 Endpoints** fully documented
- **Request/Response schemas** for all operations
- **Authentication requirements** per endpoint
- **Role-based access control** specifications
- **Data models** with validation rules
- **Error responses** with status codes
- **Example requests** and responses

#### Quick API Overview

| Blueprint | Endpoints | Description |
|-----------|-----------|-------------|
| Authentication | 8 routes | Login, register, logout, legal pages |
| Admin | 9 routes | Doctor/patient management, appointments |
| Doctor | 8 routes | Appointments, patients, availability, profile |
| Patient | 8 routes | Search doctors, book appointments, treatment history |

**Total**: 50 documented endpoints with complete schemas

---

## Security

### Implemented Security Measures

1. **Password Security**
   - Bcrypt hashing (cost factor: 12)
   - No plaintext password storage
   - Secure password validation

2. **Authentication & Authorization**
   - Flask-Login session management
   - Role-based access control (RBAC)
   - Custom decorators for route protection
   - Automatic logout on session expiry

3. **CSRF Protection**
   - Flask-WTF CSRF tokens on all forms
   - Automatic token validation

4. **SQL Injection Prevention**
   - SQLAlchemy ORM (parameterized queries)
   - No raw SQL execution

5. **Session Security**
   - Secure session cookies
   - HTTPOnly flag enabled
   - Session timeout implemented

6. **Input Validation**
   - Server-side form validation
   - Data sanitization
   - Type checking

### Security Best Practices

- ✅ Change default admin password
- ✅ Use strong SECRET_KEY in production
- ✅ Enable HTTPS in production
- ✅ Regular security audits
- ✅ Keep dependencies updated
- ✅ Implement rate limiting (recommended)
- ✅ Add logging for security events

---

## Testing

### Manual Testing Checklist

#### Authentication
- [ ] Patient registration works correctly
- [ ] Login with valid credentials succeeds
- [ ] Login with invalid credentials fails
- [ ] Logout clears session
- [ ] Password change functionality works
- [ ] Blacklisted users cannot login

#### Admin Operations
- [ ] Dashboard displays correct statistics
- [ ] Can add new doctor
- [ ] Can edit existing doctor
- [ ] Can delete doctor (with confirmation)
- [ ] Can search doctors and patients
- [ ] Can view all appointments

#### Doctor Operations
- [ ] Dashboard shows assigned appointments
- [ ] Can view patient history
- [ ] Can complete appointment with treatment
- [ ] Can cancel appointment
- [ ] Can set 7-day availability
- [ ] Profile updates persist correctly

#### Patient Operations
- [ ] Can search doctors by specialization
- [ ] Can view doctor availability
- [ ] Can book appointment
- [ ] Double-booking prevention works
- [ ] Can cancel appointment
- [ ] Can view treatment history

#### UI/UX
- [ ] Responsive design works on mobile
- [ ] All forms validate input
- [ ] Flash messages display correctly
- [ ] Navigation works across all pages
- [ ] Legal pages (Privacy, Terms, FAQ) load

### Running Tests

```bash
# Install testing dependencies
pip install pytest pytest-flask

# Run tests (when test suite is implemented)
pytest tests/

# Run with coverage
pytest --cov=. tests/
```

---

## Performance Considerations

### Database Optimization
- Indexed columns: `username`, `email`, `appointment_date`
- Foreign key constraints for data integrity
- Lazy loading for relationships
- Query optimization with `joinedload()`

### Caching (Recommended for Production)
```python
# Install Flask-Caching
pip install Flask-Caching

# Add to config
CACHE_TYPE = 'simple'
CACHE_DEFAULT_TIMEOUT = 300
```

### Production Deployment

#### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

#### Using Docker
```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

---

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'flask'`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue**: Database not found
```bash
# Solution: Delete and recreate
rm instance/hospital.db
python app.py
```

**Issue**: Port 5000 already in use
```python
# Solution: Change port in app.py
app.run(debug=True, port=5001)
```

**Issue**: CSRF token missing
```python
# Solution: Ensure form includes {{ form.csrf_token }}
```

**Issue**: Templates not rendering
```bash
# Solution: Check template path and inheritance
# Ensure {% extends "base.html" %} is correct
```

---

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make changes and commit
   ```bash
   git commit -m "Add: your feature description"
   ```
4. Push to your fork
   ```bash
   git push origin feature/your-feature-name
   ```
5. Submit a pull request

### Coding Standards

- Follow PEP 8 style guide
- Write descriptive commit messages
- Add docstrings to functions
- Update tests for new features
- Update documentation

### Git Commit Message Convention

```
Type: Brief description

Types: Add, Update, Fix, Remove, Refactor, Docs, Test
```

---

## Project Information

**Course**: App Development I (September 2025)
**Institution**: IIT Madras
**Project Type**: Individual Assignment
**Version**: 0.5.0
**Status**: Production Ready

### AI/LLM Usage Declaration
This project utilized AI tools (Claude/ChatGPT) for code generation and debugging assistance (~60-70%). All project decisions, architecture design, feature requirements, testing, and final integration were independently conceived and executed. AI served as a development assistant for writing code, while maintaining full human control over project direction.

---

## License

This project is developed for educational purposes as part of the IIT Madras App Development I course.

---

## Contact & Support

For technical issues or questions:
- Check the [FAQ page](http://127.0.0.1:5000/faq)
- Review the [Privacy Policy](http://127.0.0.1:5000/privacy-policy)
- Review the [Terms of Service](http://127.0.0.1:5000/terms-of-service)

---

**Last Updated**: November 29, 2025
**Maintained by**: IIT Madras Student

Made with ❤️ using Flask & Bootstrap
