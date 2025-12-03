# Database Schema Documentation

## Overview
This document describes the complete database schema for the Hospital Management System.

## Database: SQLite (hospital.db)

---

## Tables

### 1. Users Table
**Purpose:** Base authentication table for all users

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique user identifier |
| username | VARCHAR(80) | UNIQUE, NOT NULL | User login name |
| email | VARCHAR(120) | UNIQUE, NOT NULL | User email address |
| password_hash | VARCHAR(255) | NOT NULL | Hashed password |
| role | VARCHAR(20) | NOT NULL | User role (admin/doctor/patient) |
| is_active | BOOLEAN | DEFAULT TRUE | Account status (for blacklisting) |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Account creation date |

---

### 2. Admin Table
**Purpose:** Store admin-specific information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique admin identifier |
| user_id | INTEGER | FOREIGN KEY → Users(id), UNIQUE | Link to Users table |
| name | VARCHAR(100) | NOT NULL | Admin full name |
| contact_number | VARCHAR(15) | - | Admin contact number |

---

### 3. Specialization Table
**Purpose:** Store medical departments/specializations

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique specialization ID |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Specialization name |
| description | TEXT | - | Department description |

**Sample Data:**
- Cardiology
- Neurology
- Orthopedics
- Pediatrics
- Dermatology
- General Medicine

---

### 4. Doctor Table
**Purpose:** Store doctor-specific information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique doctor identifier |
| user_id | INTEGER | FOREIGN KEY → Users(id), UNIQUE | Link to Users table |
| name | VARCHAR(100) | NOT NULL | Doctor full name |
| specialization_id | INTEGER | FOREIGN KEY → Specialization(id) | Medical specialization |
| qualification | VARCHAR(200) | - | Degrees and certifications |
| experience_years | INTEGER | - | Years of experience |
| contact_number | VARCHAR(15) | - | Doctor contact number |
| profile_image | VARCHAR(255) | - | Profile picture path (optional) |

---

### 5. Patient Table
**Purpose:** Store patient-specific information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique patient identifier |
| user_id | INTEGER | FOREIGN KEY → Users(id), UNIQUE | Link to Users table |
| name | VARCHAR(100) | NOT NULL | Patient full name |
| date_of_birth | DATE | - | Patient DOB |
| gender | VARCHAR(10) | - | Male/Female/Other |
| contact_number | VARCHAR(15) | NOT NULL | Patient contact number |
| address | TEXT | - | Residential address |
| blood_group | VARCHAR(5) | - | Blood type |
| emergency_contact | VARCHAR(15) | - | Emergency contact number |

---

### 6. Doctor_Availability Table
**Purpose:** Track doctor availability for next 7 days

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique availability record |
| doctor_id | INTEGER | FOREIGN KEY → Doctor(id) | Doctor reference |
| available_date | DATE | NOT NULL | Available date |
| start_time | TIME | NOT NULL | Availability start time |
| end_time | TIME | NOT NULL | Availability end time |
| is_available | BOOLEAN | DEFAULT TRUE | Availability status |

**Notes:**
- Doctors set availability for next 7 days
- Multiple time slots per day allowed
- Used for preventing double-booking

---

### 7. Appointment Table
**Purpose:** Store all appointment bookings

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique appointment ID |
| patient_id | INTEGER | FOREIGN KEY → Patient(id) | Patient reference |
| doctor_id | INTEGER | FOREIGN KEY → Doctor(id) | Doctor reference |
| appointment_date | DATE | NOT NULL | Appointment date |
| appointment_time | TIME | NOT NULL | Appointment time |
| status | VARCHAR(20) | NOT NULL | Booked/Completed/Cancelled |
| booking_date | DATETIME | DEFAULT CURRENT_TIMESTAMP | When booking was made |
| cancellation_reason | TEXT | - | Reason if cancelled |

**Constraints:**
- UNIQUE(doctor_id, appointment_date, appointment_time) where status='Booked'
- Prevents double-booking

**Status Flow:**
```
Booked → Completed
Booked → Cancelled
```

---

### 8. Treatment Table
**Purpose:** Store medical treatment records

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique treatment record |
| appointment_id | INTEGER | FOREIGN KEY → Appointment(id), UNIQUE | Link to appointment |
| diagnosis | TEXT | NOT NULL | Medical diagnosis |
| prescription | TEXT | - | Prescribed medications |
| notes | TEXT | - | Doctor's notes |
| treatment_date | DATETIME | DEFAULT CURRENT_TIMESTAMP | When treatment was recorded |

**Notes:**
- One treatment record per completed appointment
- Created when doctor marks appointment as "Completed"

---

## Relationships

### ER Diagram Description

```
Users (1) ←→ (1) Admin
Users (1) ←→ (1) Doctor
Users (1) ←→ (1) Patient

Specialization (1) ←→ (N) Doctor

Doctor (1) ←→ (N) Appointment
Patient (1) ←→ (N) Appointment
Doctor (1) ←→ (N) Doctor_Availability

Appointment (1) ←→ (1) Treatment
```

---

## Indexes (For Performance)

```sql
CREATE INDEX idx_appointment_doctor ON Appointment(doctor_id);
CREATE INDEX idx_appointment_patient ON Appointment(patient_id);
CREATE INDEX idx_appointment_date ON Appointment(appointment_date);
CREATE INDEX idx_doctor_specialization ON Doctor(specialization_id);
CREATE INDEX idx_availability_doctor_date ON Doctor_Availability(doctor_id, available_date);
```

---

## Default Data

### Admin User (Programmatically Created)
```python
username: admin
email: admin@hospital.com
password: admin123
role: admin
```

### Sample Specializations
```python
[
    "Cardiology",
    "Neurology",
    "Orthopedics",
    "Pediatrics",
    "Dermatology",
    "General Medicine",
    "ENT",
    "Psychiatry"
]
```

---

## Database Initialization Code Location
**File:** `utils/database.py`
**Function:** `init_db()`

This function:
1. Creates all tables using SQLAlchemy models
2. Inserts default admin user
3. Inserts default specializations
4. Should run on first application startup

---

**Last Updated:** 2025-11-26
