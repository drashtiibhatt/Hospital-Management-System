# User Guide - Hospital Management System

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Admin Guide](#admin-guide)
4. [Doctor Guide](#doctor-guide)
5. [Patient Guide](#patient-guide)
6. [Common Operations](#common-operations)
7. [FAQs](#faqs)

---

## Introduction

The Hospital Management System (HMS) is a web application designed to streamline hospital operations by managing patients, doctors, appointments, and medical records.

### User Roles
- **Admin:** Hospital staff with full system access
- **Doctor:** Medical professionals who treat patients
- **Patient:** Users seeking medical care

---

## Getting Started

### Accessing the Application

1. Open your web browser
2. Navigate to: `http://127.0.0.1:5000/`
3. You will see the landing page with login and register options

### First-Time Users

**For Patients:**
- Click "Register" button
- Fill out the registration form
- Create an account with username and password
- Login to access the patient dashboard

**For Doctors:**
- Your account will be created by the Admin
- Use the credentials provided by the hospital
- Login to access the doctor dashboard

**For Admin:**
- Default admin account already exists
- Username: `admin`
- Password: `admin123`

---

## Admin Guide

### Logging In

1. Click "Login" button
2. Enter admin credentials
3. Click "Submit"
4. You'll be redirected to the Admin Dashboard

### Admin Dashboard

The dashboard displays:
- Total number of doctors
- Total number of patients
- Total number of appointments
- Quick action buttons

---

### Managing Doctors

#### Adding a New Doctor

1. Go to "Manage Doctors" from the navigation menu
2. Click "Add New Doctor" button
3. Fill in the form:
   - Name
   - Email
   - Username
   - Password
   - Specialization (select from dropdown)
   - Qualification
   - Experience (years)
   - Contact Number
4. Click "Add Doctor"
5. Success message will appear

#### Editing Doctor Information

1. Go to "Manage Doctors"
2. Find the doctor in the list
3. Click "Edit" button
4. Update the required fields
5. Click "Save Changes"

#### Removing a Doctor

1. Go to "Manage Doctors"
2. Find the doctor in the list
3. Click "Delete" button
4. Confirm deletion
5. Doctor will be removed from the system

---

### Managing Patients

#### Viewing All Patients

1. Go to "Manage Patients" from the menu
2. View the list of all registered patients
3. See patient details: Name, Contact, Registration Date

#### Editing Patient Information

1. Find the patient in the list
2. Click "Edit" button
3. Update necessary information
4. Click "Save Changes"

#### Blacklisting a Patient

1. Find the patient in the list
2. Click "Blacklist" button
3. Confirm action
4. Patient will no longer be able to login

---

### Managing Appointments

#### Viewing All Appointments

1. Go to "View Appointments" from the menu
2. See all upcoming and past appointments
3. Filter by:
   - Date
   - Doctor
   - Patient
   - Status (Booked/Completed/Cancelled)

#### Appointment Details

Each appointment shows:
- Patient name
- Doctor name
- Date and time
- Status
- Booking date

---

### Search Functionality

#### Searching for Doctors

1. Use the search bar in "Manage Doctors"
2. Search by:
   - Doctor name
   - Specialization
3. Results appear instantly

#### Searching for Patients

1. Use the search bar in "Manage Patients"
2. Search by:
   - Patient name
   - Patient ID
   - Contact number
3. Results appear instantly

---

## Doctor Guide

### Logging In

1. Click "Login" button
2. Enter your doctor credentials
3. Click "Submit"
4. You'll be redirected to the Doctor Dashboard

### Doctor Dashboard

The dashboard displays:
- Your upcoming appointments for today/week
- List of patients assigned to you
- Quick statistics

---

### Managing Appointments

#### Viewing Your Appointments

1. Dashboard shows all your appointments
2. Filter by:
   - Today's appointments
   - This week's appointments
   - All appointments

#### Appointment Details

Each appointment shows:
- Patient name
- Appointment date and time
- Status
- Patient contact information

---

### Completing an Appointment

1. Find the appointment in your list
2. Click "Complete" button
3. Fill in the treatment form:
   - **Diagnosis:** Medical findings
   - **Prescription:** Medications prescribed
   - **Notes:** Additional doctor notes
4. Click "Save Treatment"
5. Appointment status changes to "Completed"

---

### Cancelling an Appointment

1. Find the appointment in your list
2. Click "Cancel" button
3. Enter cancellation reason
4. Click "Confirm"
5. Patient will be notified

---

### Viewing Patient History

1. Click on a patient's name in your appointments
2. View their complete medical history:
   - Past appointments
   - Previous diagnoses
   - Past prescriptions
   - Doctor notes
3. This helps in making informed decisions

---

### Setting Your Availability

#### Managing 7-Day Availability

1. Go to "My Availability" from the menu
2. Select the dates you're available (next 7 days)
3. For each date, set:
   - Start time
   - End time
4. Click "Save Availability"
5. Patients can only book during these slots

#### Updating Availability

1. Go to "My Availability"
2. Edit existing time slots
3. Add new time slots
4. Remove unavailable slots
5. Click "Update"

---

## Patient Guide

### Registering an Account

1. Click "Register" button on the homepage
2. Fill in the registration form:
   - Full Name
   - Email
   - Username
   - Password
   - Date of Birth
   - Gender
   - Contact Number
   - Address
   - Blood Group (optional)
   - Emergency Contact
3. Click "Register"
4. Login with your credentials

### Patient Dashboard

The dashboard displays:
- Available specializations
- Your upcoming appointments
- Quick action buttons

---

### Searching for Doctors

#### By Specialization

1. Dashboard shows all specializations
2. Click on a specialization (e.g., Cardiology)
3. View all doctors in that field
4. See doctor details:
   - Name
   - Qualification
   - Experience
   - Available time slots

#### By Doctor Name

1. Use the search bar
2. Type doctor's name
3. View search results
4. Click on doctor to see profile

---

### Booking an Appointment

1. Find the doctor you want to consult
2. View their 7-day availability
3. Select:
   - Date
   - Time slot
4. Click "Book Appointment"
5. Confirm booking
6. Success message appears
7. Appointment added to "My Appointments"

#### Important Notes
- You can only book during doctor's available slots
- Cannot book the same doctor at the same time
- Appointments are marked as "Booked" initially

---

### Managing Your Appointments

#### Viewing Upcoming Appointments

1. Go to "My Appointments"
2. See all your booked appointments
3. Details shown:
   - Doctor name
   - Date and time
   - Status
   - Specialization

#### Cancelling an Appointment

1. Go to "My Appointments"
2. Find the appointment
3. Click "Cancel" button
4. Confirm cancellation
5. Status changes to "Cancelled"

**Note:** You cannot cancel completed appointments.

---

### Viewing Treatment History

1. Go to "Treatment History" from the menu
2. See all past completed appointments
3. For each appointment, view:
   - Date of visit
   - Doctor name
   - Diagnosis
   - Prescription
   - Doctor's notes
4. You can download or print this history

---

### Editing Your Profile

1. Click on "My Profile" in the navigation
2. Update your information:
   - Contact number
   - Address
   - Emergency contact
3. Click "Save Changes"

**Note:** You cannot change your username or email.

---

## Common Operations

### Changing Your Password

1. Login to your account
2. Go to "Settings" or "Profile"
3. Click "Change Password"
4. Enter:
   - Current password
   - New password
   - Confirm new password
5. Click "Update Password"

---

### Logging Out

1. Click on your name in the top-right corner
2. Select "Logout" from the dropdown
3. You'll be redirected to the homepage

---

## FAQs

### General Questions

**Q: Who can access the system?**
A: Admin, Doctors, and Patients can access the system with their respective credentials.

**Q: Is my data secure?**
A: Yes, passwords are encrypted, and the system uses secure sessions.

**Q: Can I use this on mobile?**
A: Yes, the system is responsive and works on mobile browsers.

---

### Admin FAQs

**Q: How do I reset a doctor's password?**
A: Edit the doctor's profile and set a new password.

**Q: Can I see deleted records?**
A: No, deleted records are permanently removed.

**Q: How do I reactivate a blacklisted user?**
A: Edit the user's profile and change their status to "Active".

---

### Doctor FAQs

**Q: Can I edit a completed appointment?**
A: No, but you can add additional notes to the treatment record.

**Q: How do I set my availability for more than 7 days?**
A: The system is designed for rolling 7-day availability. Update it weekly.

**Q: Can I see other doctors' appointments?**
A: No, you can only see your own appointments.

---

### Patient FAQs

**Q: Can I book multiple appointments with the same doctor?**
A: Yes, as long as they're at different times.

**Q: Can I reschedule an appointment?**
A: Cancel the existing appointment and book a new one.

**Q: How do I get my treatment history?**
A: Go to "Treatment History" in your dashboard.

**Q: What if a doctor cancels my appointment?**
A: You'll see the status as "Cancelled" and can book a new one.

**Q: Can I choose a specific doctor?**
A: Yes, you can search and select any available doctor.

---

## Support

If you encounter any issues or need help:
- Contact the hospital admin
- Check the documentation
- Report bugs to the development team

---

**User Guide Version:** 1.0
**Last Updated:** 2025-11-26
