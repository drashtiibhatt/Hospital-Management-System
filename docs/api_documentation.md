# API Documentation

**Status:** Optional Feature - To Be Implemented

This document outlines the REST API endpoints for the Hospital Management System (if implemented).

---

## Base URL

```
http://127.0.0.1:5000/api/v1
```

---

## Authentication

All API endpoints require authentication. Include the session cookie or token in the request headers.

```
Cookie: session=<session_id>
```

---

## Response Format

All responses are in JSON format.

### Success Response

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful"
}
```

### Error Response

```json
{
  "success": false,
  "error": "Error message",
  "code": 400
}
```

---

## API Endpoints

### 1. Doctor Endpoints

#### GET /api/v1/doctors

Get all doctors.

**Query Parameters:**
- `specialization` (optional): Filter by specialization ID
- `search` (optional): Search by name

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Dr. John Smith",
      "specialization": "Cardiology",
      "qualification": "MD, DM Cardiology",
      "experience_years": 15,
      "contact_number": "1234567890"
    }
  ]
}
```

---

#### GET /api/v1/doctors/:id

Get a specific doctor by ID.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Dr. John Smith",
    "specialization": "Cardiology",
    "qualification": "MD, DM Cardiology",
    "experience_years": 15,
    "contact_number": "1234567890",
    "availability": [
      {
        "date": "2025-11-27",
        "start_time": "09:00",
        "end_time": "17:00"
      }
    ]
  }
}
```

---

#### POST /api/v1/doctors

Create a new doctor (Admin only).

**Request Body:**
```json
{
  "name": "Dr. Jane Doe",
  "email": "jane@hospital.com",
  "username": "janedoe",
  "password": "securepass123",
  "specialization_id": 2,
  "qualification": "MD, DNB",
  "experience_years": 10,
  "contact_number": "9876543210"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 2,
    "name": "Dr. Jane Doe"
  },
  "message": "Doctor created successfully"
}
```

---

#### PUT /api/v1/doctors/:id

Update doctor information (Admin only).

**Request Body:**
```json
{
  "name": "Dr. Jane Doe Updated",
  "contact_number": "9999999999"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Doctor updated successfully"
}
```

---

#### DELETE /api/v1/doctors/:id

Delete a doctor (Admin only).

**Response:**
```json
{
  "success": true,
  "message": "Doctor deleted successfully"
}
```

---

### 2. Patient Endpoints

#### GET /api/v1/patients

Get all patients (Admin only).

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "John Patient",
      "contact_number": "1231231234",
      "blood_group": "O+",
      "gender": "Male"
    }
  ]
}
```

---

#### GET /api/v1/patients/:id

Get a specific patient by ID.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "John Patient",
    "date_of_birth": "1990-01-01",
    "gender": "Male",
    "contact_number": "1231231234",
    "address": "123 Main St",
    "blood_group": "O+",
    "emergency_contact": "9999999999"
  }
}
```

---

#### POST /api/v1/patients

Register a new patient.

**Request Body:**
```json
{
  "name": "New Patient",
  "email": "patient@example.com",
  "username": "newpatient",
  "password": "securepass123",
  "date_of_birth": "1995-05-15",
  "gender": "Female",
  "contact_number": "5555555555",
  "address": "456 Oak Ave",
  "blood_group": "A+",
  "emergency_contact": "8888888888"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 2,
    "name": "New Patient"
  },
  "message": "Patient registered successfully"
}
```

---

#### PUT /api/v1/patients/:id

Update patient information.

**Request Body:**
```json
{
  "contact_number": "6666666666",
  "address": "789 Pine St"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Patient updated successfully"
}
```

---

### 3. Appointment Endpoints

#### GET /api/v1/appointments

Get all appointments.

**Query Parameters:**
- `patient_id` (optional): Filter by patient
- `doctor_id` (optional): Filter by doctor
- `status` (optional): Filter by status (Booked/Completed/Cancelled)
- `date` (optional): Filter by date

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "patient_name": "John Patient",
      "doctor_name": "Dr. John Smith",
      "appointment_date": "2025-11-27",
      "appointment_time": "10:00",
      "status": "Booked"
    }
  ]
}
```

---

#### GET /api/v1/appointments/:id

Get a specific appointment by ID.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "patient_id": 1,
    "patient_name": "John Patient",
    "doctor_id": 1,
    "doctor_name": "Dr. John Smith",
    "appointment_date": "2025-11-27",
    "appointment_time": "10:00",
    "status": "Booked",
    "booking_date": "2025-11-25T14:30:00"
  }
}
```

---

#### POST /api/v1/appointments

Book a new appointment.

**Request Body:**
```json
{
  "patient_id": 1,
  "doctor_id": 1,
  "appointment_date": "2025-11-28",
  "appointment_time": "11:00"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 2,
    "appointment_date": "2025-11-28",
    "appointment_time": "11:00"
  },
  "message": "Appointment booked successfully"
}
```

**Error Response (Double Booking):**
```json
{
  "success": false,
  "error": "Doctor is not available at this time",
  "code": 409
}
```

---

#### PUT /api/v1/appointments/:id

Update appointment (cancel or complete).

**Request Body (Cancel):**
```json
{
  "status": "Cancelled",
  "cancellation_reason": "Patient not available"
}
```

**Request Body (Complete with Treatment):**
```json
{
  "status": "Completed",
  "treatment": {
    "diagnosis": "Common cold",
    "prescription": "Paracetamol 500mg, TID for 3 days",
    "notes": "Rest and drink plenty of fluids"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Appointment updated successfully"
}
```

---

#### DELETE /api/v1/appointments/:id

Cancel an appointment.

**Response:**
```json
{
  "success": true,
  "message": "Appointment cancelled successfully"
}
```

---

### 4. Specialization Endpoints

#### GET /api/v1/specializations

Get all specializations.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Cardiology",
      "description": "Heart and cardiovascular system",
      "doctors_count": 5
    },
    {
      "id": 2,
      "name": "Neurology",
      "description": "Brain and nervous system",
      "doctors_count": 3
    }
  ]
}
```

---

### 5. Treatment Endpoints

#### GET /api/v1/treatments/patient/:patient_id

Get treatment history for a patient.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "appointment_id": 1,
      "doctor_name": "Dr. John Smith",
      "appointment_date": "2025-11-20",
      "diagnosis": "Hypertension",
      "prescription": "Amlodipine 5mg, OD",
      "notes": "Follow up in 2 weeks",
      "treatment_date": "2025-11-20T15:00:00"
    }
  ]
}
```

---

## HTTP Status Codes

- `200 OK` - Successful GET request
- `201 Created` - Successful POST request
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource conflict (e.g., double booking)
- `500 Internal Server Error` - Server error

---

## Error Codes

| Code | Description |
|------|-------------|
| 1001 | Invalid credentials |
| 1002 | User not found |
| 1003 | Unauthorized access |
| 2001 | Doctor not found |
| 2002 | Doctor not available |
| 3001 | Patient not found |
| 4001 | Appointment not found |
| 4002 | Appointment already booked |
| 4003 | Cannot modify completed appointment |

---

## Rate Limiting

(To be implemented if needed)

- 100 requests per minute per user
- 429 Too Many Requests response if exceeded

---

## Pagination

For endpoints returning lists, use pagination:

**Query Parameters:**
- `page` (default: 1)
- `per_page` (default: 20, max: 100)

**Response:**
```json
{
  "success": true,
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 50,
    "pages": 3
  }
}
```

---

## Implementation Notes

### Using Flask-RESTful

```python
from flask_restful import Resource, Api

api = Api(app)

class DoctorListAPI(Resource):
    def get(self):
        # Get all doctors
        pass

    def post(self):
        # Create new doctor
        pass

api.add_resource(DoctorListAPI, '/api/v1/doctors')
```

### Alternative: JSON from Controllers

```python
from flask import jsonify

@app.route('/api/v1/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify({
        'success': True,
        'data': [doctor.to_dict() for doctor in doctors]
    })
```

---

## Testing APIs

### Using cURL

```bash
# GET request
curl http://127.0.0.1:5000/api/v1/doctors

# POST request
curl -X POST http://127.0.0.1:5000/api/v1/doctors \
  -H "Content-Type: application/json" \
  -d '{"name":"Dr. Test","email":"test@hospital.com"}'
```

### Using Postman

1. Import the API collection
2. Set the base URL
3. Test each endpoint with sample data

---

**API Version:** 1.0 (Optional)
**Status:** Not Yet Implemented
**Last Updated:** 2025-11-26
