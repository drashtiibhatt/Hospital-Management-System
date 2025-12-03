# Hospital Management System - Project Report

**IIT Madras - App Development I (Sept 2025)**

---

## Author

**Name:** [Your Full Name]
**Roll Number:** [Your Roll Number]
**Email:** [Your Email]@study.iitm.ac.in

I am a student pursuing the BS in Data Science and Applications program at IIT Madras. This project represents my work in applying web development concepts to create a practical healthcare management solution using Flask framework and modern web technologies.

---

## Description

The Hospital Management System is a comprehensive web application designed to streamline hospital operations by managing three distinct user roles: Admins (hospital staff), Doctors, and Patients. The system enables efficient appointment scheduling, patient record management, treatment history tracking, and doctor availability management. It addresses real-world challenges in healthcare administration by providing a centralized platform for appointment booking, medical record keeping, and hospital resource management with role-based access control and double-booking prevention.

---

## Technologies Used

### Backend Technologies
- **Flask 3.0.0** - Python web framework chosen for its lightweight nature and MVC architecture support
- **Flask-SQLAlchemy** - ORM for database operations, preventing SQL injection and simplifying database queries
- **Flask-Login** - User session management and authentication, providing secure login/logout functionality
- **Flask-Bcrypt** - Password hashing using bcrypt algorithm for secure password storage
- **SQLite** - Lightweight relational database, ideal for development and small to medium deployments

### Frontend Technologies
- **Jinja2** - Template engine for dynamic HTML rendering with Python integration
- **Bootstrap 5.3.0** - CSS framework for responsive design and modern UI components
- **HTML5/CSS3** - Standard web technologies for structure and styling
- **JavaScript (Vanilla)** - Client-side interactivity for dynamic form handling and validation

### Purpose & Rationale
Flask was selected for its simplicity and flexibility in building MVC applications. SQLAlchemy provides database abstraction and security through parameterized queries. Bootstrap 5 enables rapid development of responsive, mobile-friendly interfaces without external JavaScript libraries. The technology stack balances development speed with production readiness while maintaining code maintainability.

---

## Database Schema Design

### Tables and Structure

#### 1. **users** (Authentication Base Table)
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `username` (VARCHAR(80), UNIQUE, NOT NULL)
- `email` (VARCHAR(120), UNIQUE, NOT NULL)
- `password_hash` (VARCHAR(128), NOT NULL)
- `role` (VARCHAR(20), NOT NULL) - Values: 'admin', 'doctor', 'patient'
- `is_active` (BOOLEAN, DEFAULT TRUE)
- `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)

#### 2. **admin**
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `user_id` (INTEGER, FOREIGN KEY → users.id, UNIQUE, NOT NULL)
- `name` (VARCHAR(100), NOT NULL)
- `contact_number` (VARCHAR(15), NOT NULL)

#### 3. **specializations**
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `name` (VARCHAR(100), UNIQUE, NOT NULL)
- `description` (TEXT)

#### 4. **doctors**
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `user_id` (INTEGER, FOREIGN KEY → users.id, UNIQUE, NOT NULL)
- `name` (VARCHAR(100), NOT NULL)
- `specialization_id` (INTEGER, FOREIGN KEY → specializations.id, NOT NULL)
- `license_number` (VARCHAR(50), UNIQUE)
- `qualification` (VARCHAR(200))
- `experience_years` (INTEGER)
- `contact_number` (VARCHAR(15), NOT NULL)
- `consultation_fee` (FLOAT, DEFAULT 500.0)
- `bio` (TEXT)

#### 5. **patients**
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `user_id` (INTEGER, FOREIGN KEY → users.id, UNIQUE, NOT NULL)
- `name` (VARCHAR(100), NOT NULL)
- `date_of_birth` (DATE, NOT NULL)
- `gender` (VARCHAR(10), NOT NULL)
- `contact_number` (VARCHAR(15), NOT NULL)
- `address` (TEXT)
- `blood_group` (VARCHAR(5))
- `emergency_contact` (VARCHAR(15))

#### 6. **doctor_availability**
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `doctor_id` (INTEGER, FOREIGN KEY → doctors.id, NOT NULL)
- `available_date` (DATE, NOT NULL)
- `start_time` (TIME, NOT NULL)
- `end_time` (TIME, NOT NULL)
- UNIQUE CONSTRAINT on (doctor_id, available_date, start_time)

#### 7. **appointments**
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `patient_id` (INTEGER, FOREIGN KEY → patients.id, NOT NULL)
- `doctor_id` (INTEGER, FOREIGN KEY → doctors.id, NOT NULL)
- `appointment_date` (DATE, NOT NULL)
- `appointment_time` (TIME, NOT NULL)
- `status` (VARCHAR(20), DEFAULT 'Booked') - Values: 'Booked', 'Completed', 'Cancelled'
- `reason` (TEXT)
- `booking_date` (DATETIME, DEFAULT CURRENT_TIMESTAMP)
- UNIQUE CONSTRAINT on (doctor_id, appointment_date, appointment_time)

#### 8. **treatments**
- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `appointment_id` (INTEGER, FOREIGN KEY → appointments.id, UNIQUE, NOT NULL)
- `diagnosis` (TEXT, NOT NULL)
- `prescription` (TEXT, NOT NULL)
- `notes` (TEXT)
- `treatment_date` (DATETIME, DEFAULT CURRENT_TIMESTAMP)

### Design Rationale
The schema follows **Third Normal Form (3NF)** to eliminate redundancy. User authentication is centralized in the `users` table with role-based differentiation, allowing efficient polymorphic queries. The unique constraint on `(doctor_id, appointment_date, appointment_time)` prevents double-booking at the database level. One-to-one relationships (user → role-specific table) ensure data integrity. The separation of doctor availability into a dedicated table allows flexible scheduling. Foreign key constraints with CASCADE DELETE ensure referential integrity when records are removed.

---

## API Design

### RESTful API Implementation
The system implements a REST API for programmatic access to core functionalities:

**Doctor API Endpoints:**
- `GET /api/doctors` - Retrieve all active doctors with specialization details
- `GET /api/doctors/<id>` - Get specific doctor profile and availability
- `GET /api/doctors/<id>/availability` - Fetch 7-day availability schedule
- `POST /api/doctors` - Create new doctor (Admin only)
- `PUT /api/doctors/<id>` - Update doctor information (Admin only)
- `DELETE /api/doctors/<id>` - Remove doctor (Admin only)

**Patient API Endpoints:**
- `GET /api/patients/<id>` - Retrieve patient profile (Authorized only)
- `GET /api/patients/<id>/appointments` - Get patient appointment history
- `POST /api/patients` - Register new patient
- `PUT /api/patients/<id>` - Update patient information

**Appointment API Endpoints:**
- `GET /api/appointments` - List all appointments (Admin/Doctor filtered view)
- `GET /api/appointments/<id>` - Get specific appointment details
- `POST /api/appointments` - Book new appointment with conflict validation
- `PUT /api/appointments/<id>` - Update appointment status or reschedule
- `DELETE /api/appointments/<id>` - Cancel appointment

**Implementation Details:**
- **Authentication:** API key or session-based authentication
- **Response Format:** JSON with status codes (200, 201, 400, 401, 404)
- **Validation:** Server-side input validation and sanitization
- **Error Handling:** Standardized error responses with descriptive messages
- **Rate Limiting:** Prevents API abuse (configurable)

The API follows RESTful conventions with proper HTTP verbs and status codes. YAML specification provided separately for detailed endpoint documentation.

---

## Architecture and Features

### Project Organization
The application follows the **Model-View-Controller (MVC)** architectural pattern:

**Models (`models/`):** 8 SQLAlchemy ORM models (User, Admin, Doctor, Patient, Specialization, DoctorAvailability, Appointment, Treatment) defining database schema and business logic methods.

**Controllers (`controllers/`):** 4 Blueprint-based controllers (auth_controller, admin_controller, doctor_controller, patient_controller) handling HTTP requests, business logic, and response rendering. Each controller manages routes for its respective user role.

**Views (`templates/`):** 47 Jinja2 templates organized by role (admin/, doctor/, patient/) with a shared base.html providing consistent layout and navigation.

**Utilities (`utils/`):** Helper modules for database initialization (`database.py`), custom decorators (`decorators.py`), and validation functions (`helpers.py`).

**Static Assets (`static/`):** CSS stylesheets, JavaScript files, and images including professional medical carousel images.

**API Layer (`api/`):** RESTful endpoints for external integrations and mobile application support.

### Core Features Implemented

**Admin Module:**
- Dashboard with real-time statistics (total doctors, patients, appointments, pending today)
- Doctor management (CRUD operations with specialization assignment)
- Patient management (view, edit, blacklist functionality)
- Appointment oversight (view all, filter by status/date)
- Specialization management
- Search functionality across doctors and patients

**Doctor Module:**
- Personalized dashboard showing today's appointments and upcoming schedule
- Patient list with appointment history and total visit counts
- Appointment management (view, complete with treatment, cancel)
- Treatment record creation (diagnosis, prescription, notes)
- 7-day availability schedule management
- Patient medical history viewing with timeline visualization

**Patient Module:**
- Self-registration with profile management
- Advanced doctor search (by specialization, name, experience)
- Real-time doctor availability viewing (next 7 days)
- Appointment booking with time slot selection and conflict prevention
- Appointment history (upcoming and past with status indicators)
- Complete treatment history access with prescriptions
- Appointment cancellation functionality

**Security Features:**
- Bcrypt password hashing (12 rounds)
- Role-based access control with custom decorators (@admin_required, @doctor_required, @patient_required)
- CSRF protection on all forms
- SQL injection prevention via ORM
- Session-based authentication with secure cookies
- Input validation and sanitization (frontend + backend)
- User account activation/deactivation

**UI/UX Enhancements (v0.5.0):**
- Professional home page with medical image carousel and dark overlay
- Dynamic statistics cards with hover animations
- Specializations showcase with custom icons
- Featured doctors section showing top 4 by experience
- Modern 4-column footer with contact info and social media integration
- Consistent white navigation across all dashboards
- Responsive design working on desktop, tablet, and mobile
- Empty states for better user experience
- Timeline components for medical history visualization
- Print-friendly treatment records

**Additional Features:**
- Double-booking prevention at database and application level
- Dynamic appointment status tracking (Booked → Completed/Cancelled)
- 5 specialist demo doctors (Dermatology, Gynecology, ENT, Neurology)
- Comprehensive dummy data for realistic testing
- Admin default credentials (username: admin, password: admin123)

### Testing & Quality Assurance
All critical workflows tested including user registration, appointment booking, treatment completion, and administrative operations. 5 major bugs identified and resolved during development (variable name mismatches in dashboards, time slot loading, data display issues). System verified on Chrome, Firefox, and Edge browsers.

---

## AI/LLM Usage Declaration

**Estimated AI Usage:** ~60-70% (Code generation and debugging assistance)

**Details of AI Assistance:**
AI tools (Claude/ChatGPT) were used extensively for code generation, bug fixing, and implementing features based on my specifications and requirements. All project decisions, architecture design, feature requirements, and testing were independently conceived and executed by me. AI was used as a development assistant for writing boilerplate code, debugging issues (variable name mismatches, data display problems), implementing UI enhancements (carousel, footer redesign), and generating consistent code patterns. I reviewed, tested, and validated all AI-generated code to ensure it met project requirements and quality standards.

**Human Contribution:**
Project planning, requirement analysis, design decisions, database schema design, testing workflows, identifying bugs, directing UI/UX improvements, and final integration were entirely my own work. AI served as a coding assistant to accelerate development while I maintained full control over the project direction and implementation choices.

---

## Video Demonstration

**Video Link:** [Insert YouTube/Google Drive Link Here - Max 3 minutes]

The video demonstrates:
1. Admin login and dashboard overview
2. Doctor management (adding a new doctor)
3. Doctor login and appointment completion workflow
4. Patient registration and appointment booking
5. Treatment history viewing
6. UI enhancements (carousel, footer, navigation)

---

**Project Completion Date:** November 29, 2025
**Total Development Time:** ~15 days
**Lines of Code:** ~29,700 lines (Backend, Frontend, Documentation)
**GitHub Repository:** [If applicable]

---

*This project was developed as part of IIT Madras App Development I course requirements.*
