"""
Database Utility Functions
Handles database initialization and seed data
"""

from models.user import User
from models.admin import Admin
from models.doctor import Doctor
from models.patient import Patient
from models.specialization import Specialization


def init_db(db, bcrypt):
    """
    Initialize database with default data
    - Creates default admin user
    - Creates default specializations
    - Seeds sample data for testing
    Should be called after db.create_all()

    Args:
        db: SQLAlchemy database instance
        bcrypt: Bcrypt instance for password hashing
    """
    print("Initializing database...")

    # Create default specializations
    create_default_specializations(db)

    # Create default admin user
    create_default_admin(db, bcrypt)

    # Create demo doctor user
    create_demo_doctor(db, bcrypt)

    # Create specialist demo doctors
    create_specialist_doctors(db, bcrypt)

    # Create demo patient user
    create_demo_patient(db, bcrypt)

    # Seed sample data (appointments, treatments, additional patients)
    seed_sample_data(db, bcrypt)

    print("Database initialization complete!")


def create_default_admin(db, bcrypt):
    """
    Create default admin user programmatically
    Credentials:
        Username: admin
        Password: admin123
        Email: admin@hospital.com
    """
    from sqlalchemy.exc import IntegrityError

    try:
        # Hash the default password
        password_hash = bcrypt.generate_password_hash('admin123').decode('utf-8')

        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@hospital.com',
            password_hash=password_hash,
            role='admin'
        )
        db.session.add(admin_user)
        db.session.flush()  # Get the user ID

        # Create admin profile
        admin_profile = Admin(
            user_id=admin_user.id,
            name='System Administrator',
            contact_number='1234567890'
        )
        db.session.add(admin_profile)

        db.session.commit()
        print("[+] Default admin created successfully!")
        print("   Username: admin")
        print("   Password: admin123")
        print("   [!] Please change the password after first login!")

        return admin_user

    except IntegrityError:
        # Admin already exists
        db.session.rollback()
        print("[i] Default admin already exists. Skipping creation.")
        return None
    except Exception as e:
        db.session.rollback()
        print(f"[X] Error creating default admin: {str(e)}")
        return None


def create_default_specializations(db):
    """
    Create default medical specializations

    Args:
        db: SQLAlchemy database instance
    """
    from sqlalchemy.exc import IntegrityError

    specializations_data = [
        {
            'name': 'General Medicine',
            'description': 'General medical consultation and treatment'
        },
        {
            'name': 'Cardiology',
            'description': 'Heart and cardiovascular system'
        },
        {
            'name': 'Neurology',
            'description': 'Brain and nervous system'
        },
        {
            'name': 'Orthopedics',
            'description': 'Bones, joints, and muscles'
        },
        {
            'name': 'Pediatrics',
            'description': 'Medical care for infants, children, and adolescents'
        },
        {
            'name': 'Dermatology',
            'description': 'Skin, hair, and nails'
        },
        {
            'name': 'ENT (Ear, Nose, Throat)',
            'description': 'Ear, nose, throat, and related structures'
        },
        {
            'name': 'Psychiatry',
            'description': 'Mental health and behavioral disorders'
        },
        {
            'name': 'Gynecology',
            'description': 'Women\'s reproductive health'
        },
        {
            'name': 'Ophthalmology',
            'description': 'Eye and vision care'
        }
    ]

    created_count = 0
    skipped_count = 0

    for spec_data in specializations_data:
        try:
            specialization = Specialization(
                name=spec_data['name'],
                description=spec_data['description']
            )
            db.session.add(specialization)
            db.session.commit()
            created_count += 1

        except IntegrityError:
            # Specialization already exists (unique constraint violation)
            db.session.rollback()
            skipped_count += 1
        except Exception as e:
            print(f"[X] Error creating specialization {spec_data['name']}: {str(e)}")
            db.session.rollback()
            continue

    if created_count > 0:
        print(f"[+] Created {created_count} specializations")

    if skipped_count > 0:
        print(f"[i] {skipped_count} specializations already exist")


def create_demo_doctor(db, bcrypt):
    """
    Create demo doctor user
    Credentials:
        Username: doctor
        Password: doctor123
        Email: doctor@hospital.com
    """
    from sqlalchemy.exc import IntegrityError

    try:
        # Hash the password
        password_hash = bcrypt.generate_password_hash('doctor123').decode('utf-8')

        # Create doctor user
        doctor_user = User(
            username='doctor',
            email='doctor@hospital.com',
            password_hash=password_hash,
            role='doctor'
        )
        db.session.add(doctor_user)
        db.session.flush()

        # Get first specialization (General Medicine)
        first_spec = Specialization.query.first()

        # Create doctor profile
        doctor_profile = Doctor(
            user_id=doctor_user.id,
            name='Dr. Demo Doctor',
            specialization_id=first_spec.id if first_spec else 1,
            license_number='DOC12345',
            qualification='MBBS, MD',
            experience_years=5,
            contact_number='9876543210'
        )
        # Set additional fields
        doctor_profile.consultation_fee = 500.0
        doctor_profile.bio = 'Demo doctor account for testing purposes'
        db.session.add(doctor_profile)

        db.session.commit()
        print("[+] Demo doctor created successfully!")
        print("   Username: doctor")
        print("   Password: doctor123")

        return doctor_user

    except IntegrityError:
        db.session.rollback()
        print("[i] Demo doctor already exists. Skipping creation.")
        return None
    except Exception as e:
        db.session.rollback()
        print(f"[X] Error creating demo doctor: {str(e)}")
        return None


def create_demo_patient(db, bcrypt):
    """
    Create demo patient user
    Credentials:
        Username: patient
        Password: patient123
        Email: patient@example.com
    """
    from sqlalchemy.exc import IntegrityError
    from datetime import date

    try:
        # Hash the password
        password_hash = bcrypt.generate_password_hash('patient123').decode('utf-8')

        # Create patient user
        patient_user = User(
            username='patient',
            email='patient@example.com',
            password_hash=password_hash,
            role='patient'
        )
        db.session.add(patient_user)
        db.session.flush()

        # Create patient profile
        patient_profile = Patient(
            user_id=patient_user.id,
            name='Demo Patient',
            contact_number='9876543211',
            date_of_birth=date(1990, 1, 1),
            gender='Male',
            address='123 Demo Street, Test City',
            blood_group='O+',
            emergency_contact='9999999999'
        )
        db.session.add(patient_profile)

        db.session.commit()
        print("[+] Demo patient created successfully!")
        print("   Username: patient")
        print("   Password: patient123")

        return patient_user

    except IntegrityError:
        db.session.rollback()
        print("[i] Demo patient already exists. Skipping creation.")
        return None
    except Exception as e:
        db.session.rollback()
        print(f"[X] Error creating demo patient: {str(e)}")
        return None


def create_specialist_doctors(db, bcrypt):
    """
    Create 5 specialist demo doctors
    - Dermatologist
    - Gynecologist
    - ENT Specialist
    - Neurologist
    - Additional Dermatologist

    All with password: doctor123
    """
    from sqlalchemy.exc import IntegrityError

    # Define specialist doctors data
    specialist_doctors = [
        {
            'username': 'dr.sarah',
            'email': 'sarah.williams@hospital.com',
            'name': 'Dr. Sarah Williams',
            'specialization': 'Dermatology',
            'license': 'DERM001',
            'qualification': 'MBBS, MD (Dermatology)',
            'experience': 8,
            'contact': '9876543220',
            'fee': 600.0,
            'bio': 'Specialist in skin conditions, acne treatment, and cosmetic dermatology'
        },
        {
            'username': 'dr.emily',
            'email': 'emily.johnson@hospital.com',
            'name': 'Dr. Emily Johnson',
            'specialization': 'Gynecology',
            'license': 'GYNO001',
            'qualification': 'MBBS, MS (Obstetrics & Gynecology)',
            'experience': 12,
            'contact': '9876543221',
            'fee': 800.0,
            'bio': 'Expert in women\'s reproductive health and prenatal care'
        },
        {
            'username': 'dr.michael',
            'email': 'michael.brown@hospital.com',
            'name': 'Dr. Michael Brown',
            'specialization': 'ENT (Ear, Nose, Throat)',
            'license': 'ENT001',
            'qualification': 'MBBS, MS (ENT)',
            'experience': 10,
            'contact': '9876543222',
            'fee': 700.0,
            'bio': 'Specialized in ear, nose, throat disorders and sinus treatments'
        },
        {
            'username': 'dr.robert',
            'email': 'robert.taylor@hospital.com',
            'name': 'Dr. Robert Taylor',
            'specialization': 'Neurology',
            'license': 'NEURO001',
            'qualification': 'MBBS, DM (Neurology)',
            'experience': 15,
            'contact': '9876543223',
            'fee': 1000.0,
            'bio': 'Expert in neurological disorders, headaches, and brain conditions'
        },
        {
            'username': 'dr.jennifer',
            'email': 'jennifer.davis@hospital.com',
            'name': 'Dr. Jennifer Davis',
            'specialization': 'Dermatology',
            'license': 'DERM002',
            'qualification': 'MBBS, MD (Dermatology), Fellowship in Cosmetic Dermatology',
            'experience': 6,
            'contact': '9876543224',
            'fee': 650.0,
            'bio': 'Specialized in cosmetic dermatology and laser treatments'
        }
    ]

    created_count = 0
    skipped_count = 0

    for doctor_data in specialist_doctors:
        try:
            # Check if doctor already exists
            existing_user = User.query.filter_by(username=doctor_data['username']).first()
            if existing_user:
                skipped_count += 1
                continue

            # Hash password
            password_hash = bcrypt.generate_password_hash('doctor123').decode('utf-8')

            # Create user account
            doctor_user = User(
                username=doctor_data['username'],
                email=doctor_data['email'],
                password_hash=password_hash,
                role='doctor'
            )
            db.session.add(doctor_user)
            db.session.flush()

            # Get specialization
            specialization = Specialization.query.filter_by(
                name=doctor_data['specialization']
            ).first()

            if not specialization:
                print(f"[!] Warning: Specialization {doctor_data['specialization']} not found for {doctor_data['name']}")
                db.session.rollback()
                continue

            # Create doctor profile
            doctor_profile = Doctor(
                user_id=doctor_user.id,
                name=doctor_data['name'],
                specialization_id=specialization.id,
                license_number=doctor_data['license'],
                qualification=doctor_data['qualification'],
                experience_years=doctor_data['experience'],
                contact_number=doctor_data['contact']
            )
            # Set additional fields
            doctor_profile.consultation_fee = doctor_data['fee']
            doctor_profile.bio = doctor_data['bio']

            db.session.add(doctor_profile)
            db.session.commit()

            created_count += 1
            print(f"[+] Created specialist doctor: {doctor_data['name']} ({doctor_data['specialization']})")

        except IntegrityError:
            db.session.rollback()
            skipped_count += 1
        except Exception as e:
            db.session.rollback()
            print(f"[X] Error creating doctor {doctor_data['name']}: {str(e)}")

    if created_count > 0:
        print(f"\n[+] Created {created_count} specialist doctors")
        print("   Username pattern: dr.firstname")
        print("   Password for all: doctor123")

    if skipped_count > 0:
        print(f"[i] {skipped_count} specialist doctors already exist")


def reset_database():
    """
    [!] DANGER: Drop all tables and recreate them
    Use only in development!
    """
    print("[!] WARNING: This will delete ALL data!")
    confirmation = input("Type 'YES' to confirm: ")

    if confirmation == 'YES':
        db.drop_all()
        db.create_all()
        init_db()
        print("[+] Database reset complete!")
    else:
        print("[X] Database reset cancelled.")


def seed_sample_data(db, bcrypt):
    """
    Create sample data for testing
    - Additional dummy patients
    - Doctor availability slots
    - Sample appointments (booked, completed, cancelled)
    - Treatment records for completed appointments
    """
    from sqlalchemy.exc import IntegrityError
    from datetime import date, time, timedelta
    from models.appointment import Appointment
    from models.treatment import Treatment
    from models.doctor import DoctorAvailability

    print("\n[i] Checking for existing dummy data...")

    # Check if dummy data already exists
    existing_appointments = Appointment.query.first()
    if existing_appointments:
        print("[i] Sample data already exists. Skipping seeding.")
        return

    print("[i] Seeding sample data...")

    try:
        # Get the demo doctor and patient
        demo_doctor = Doctor.query.join(User).filter(User.username == 'doctor').first()
        demo_patient = Patient.query.join(User).filter(User.username == 'patient').first()

        if not demo_doctor or not demo_patient:
            print("[X] Demo users not found. Please create demo users first.")
            return

        # 1. Create additional dummy patients
        print("[i] Creating additional patients...")
        additional_patients = create_additional_patients(db, bcrypt)

        # 2. Create doctor availability slots (next 7 days)
        print("[i] Creating doctor availability slots...")
        create_doctor_availability(demo_doctor.id)

        # 3. Create sample appointments
        print("[i] Creating sample appointments...")
        create_sample_appointments(demo_doctor.id, demo_patient.id, additional_patients)

        db.session.commit()
        print("[+] Sample data seeding complete!")

        # Print statistics
        print("\n[i] Created:")
        print(f"    - {len(additional_patients)} additional patients")
        print(f"    - {DoctorAvailability.query.filter_by(doctor_id=demo_doctor.id).count()} availability slots")
        print(f"    - {Appointment.query.count()} appointments")
        print(f"    - {Treatment.query.count()} treatment records")

    except Exception as e:
        db.session.rollback()
        print(f"[X] Error seeding sample data: {str(e)}")


def create_additional_patients(db, bcrypt):
    """Create additional dummy patients for testing"""
    from datetime import date

    additional_patients_data = [
        {
            'username': 'john_doe',
            'email': 'john.doe@example.com',
            'password': 'patient123',
            'name': 'John Doe',
            'contact_number': '9876543212',
            'date_of_birth': date(1985, 5, 15),
            'gender': 'Male',
            'address': '456 Oak Street, Demo City',
            'blood_group': 'A+',
            'emergency_contact': '9999999998'
        },
        {
            'username': 'jane_smith',
            'email': 'jane.smith@example.com',
            'password': 'patient123',
            'name': 'Jane Smith',
            'contact_number': '9876543213',
            'date_of_birth': date(1992, 8, 20),
            'gender': 'Female',
            'address': '789 Pine Avenue, Demo City',
            'blood_group': 'B+',
            'emergency_contact': '9999999997'
        },
        {
            'username': 'robert_johnson',
            'email': 'robert.johnson@example.com',
            'password': 'patient123',
            'name': 'Robert Johnson',
            'contact_number': '9876543214',
            'date_of_birth': date(1978, 12, 10),
            'gender': 'Male',
            'address': '321 Elm Road, Demo City',
            'blood_group': 'O-',
            'emergency_contact': '9999999996'
        }
    ]

    created_patients = []

    for patient_data in additional_patients_data:
        try:
            # Create user account
            password_hash = bcrypt.generate_password_hash(patient_data['password']).decode('utf-8')
            user = User(
                username=patient_data['username'],
                email=patient_data['email'],
                password_hash=password_hash,
                role='patient'
            )
            db.session.add(user)
            db.session.flush()

            # Create patient profile
            patient = Patient(
                user_id=user.id,
                name=patient_data['name'],
                contact_number=patient_data['contact_number'],
                date_of_birth=patient_data['date_of_birth'],
                gender=patient_data['gender'],
                address=patient_data['address'],
                blood_group=patient_data['blood_group'],
                emergency_contact=patient_data['emergency_contact']
            )
            db.session.add(patient)
            db.session.flush()
            created_patients.append(patient)

        except Exception as e:
            print(f"[!] Could not create patient {patient_data['name']}: {str(e)}")
            db.session.rollback()
            continue

    return created_patients


def create_doctor_availability(doctor_id):
    """Create availability slots for demo doctor (next 7 days)"""
    from datetime import date, time, timedelta
    from extensions import db
    from models.doctor import DoctorAvailability

    today = date.today()

    # Create availability for next 7 days
    # Morning slot: 9:00 AM - 1:00 PM
    # Evening slot: 5:00 PM - 8:00 PM
    for i in range(7):
        slot_date = today + timedelta(days=i)

        # Morning slot
        morning_slot = DoctorAvailability(
            doctor_id=doctor_id,
            available_date=slot_date,
            start_time=time(9, 0),
            end_time=time(13, 0),
            is_available=True
        )
        db.session.add(morning_slot)

        # Evening slot
        evening_slot = DoctorAvailability(
            doctor_id=doctor_id,
            available_date=slot_date,
            start_time=time(17, 0),
            end_time=time(20, 0),
            is_available=True
        )
        db.session.add(evening_slot)


def create_sample_appointments(demo_doctor_id, demo_patient_id, additional_patients):
    """Create sample appointments with different statuses"""
    from datetime import date, time, timedelta
    from extensions import db
    from models.appointment import Appointment
    from models.treatment import Treatment

    today = date.today()
    appointments_data = []

    # Get all patient IDs
    all_patient_ids = [demo_patient_id] + [p.id for p in additional_patients]

    # 1. Completed appointments (past dates with treatment records)
    completed_appointments = [
        {
            'patient_id': demo_patient_id,
            'date': today - timedelta(days=10),
            'time': time(10, 0),
            'status': 'Completed',
            'diagnosis': 'Common Cold',
            'prescription': 'Paracetamol 500mg - 3 times a day for 5 days\nRest and drink plenty of fluids',
            'notes': 'Patient recovering well. Follow-up not required unless symptoms persist.'
        },
        {
            'patient_id': demo_patient_id,
            'date': today - timedelta(days=5),
            'time': time(11, 0),
            'status': 'Completed',
            'diagnosis': 'Seasonal Allergies',
            'prescription': 'Cetirizine 10mg - Once daily at bedtime\nAvoid allergen exposure',
            'notes': 'Mild allergic reaction. Antihistamine prescribed.'
        }
    ]

    if len(additional_patients) >= 1:
        completed_appointments.append({
            'patient_id': additional_patients[0].id,
            'date': today - timedelta(days=7),
            'time': time(14, 0),
            'status': 'Completed',
            'diagnosis': 'Hypertension',
            'prescription': 'Amlodipine 5mg - Once daily in the morning\nLow salt diet recommended',
            'notes': 'Blood pressure: 145/95. Started on medication. Review in 2 weeks.'
        })

    if len(additional_patients) >= 2:
        completed_appointments.append({
            'patient_id': additional_patients[1].id,
            'date': today - timedelta(days=3),
            'time': time(15, 30),
            'status': 'Completed',
            'diagnosis': 'Migraine',
            'prescription': 'Sumatriptan 50mg - As needed for migraine attacks\nStress management advised',
            'notes': 'Recurrent migraines. Prescribed triptan. Advised lifestyle modifications.'
        })

    # Create completed appointments and their treatments
    for apt_data in completed_appointments:
        appointment = Appointment(
            patient_id=apt_data['patient_id'],
            doctor_id=demo_doctor_id,
            appointment_date=apt_data['date'],
            appointment_time=apt_data['time'],
            status=apt_data['status']
        )
        db.session.add(appointment)
        db.session.flush()

        # Create treatment record
        treatment = Treatment(
            appointment_id=appointment.id,
            diagnosis=apt_data['diagnosis'],
            prescription=apt_data['prescription'],
            notes=apt_data['notes']
        )
        db.session.add(treatment)

    # 2. Upcoming booked appointments
    booked_appointments = [
        {
            'patient_id': demo_patient_id,
            'date': today,  # TODAY's appointment
            'time': time(14, 0),
            'status': 'Booked'
        },
        {
            'patient_id': demo_patient_id,
            'date': today + timedelta(days=2),
            'time': time(10, 30),
            'status': 'Booked'
        },
        {
            'patient_id': demo_patient_id,
            'date': today + timedelta(days=5),
            'time': time(18, 0),
            'status': 'Booked'
        }
    ]

    if len(additional_patients) >= 1:
        booked_appointments.extend([
            {
                'patient_id': additional_patients[0].id,
                'date': today + timedelta(days=1),
                'time': time(9, 30),
                'status': 'Booked'
            },
            {
                'patient_id': additional_patients[0].id,
                'date': today + timedelta(days=4),
                'time': time(17, 30),
                'status': 'Booked'
            }
        ])

    if len(additional_patients) >= 2:
        booked_appointments.append({
            'patient_id': additional_patients[1].id,
            'date': today + timedelta(days=3),
            'time': time(11, 30),
            'status': 'Booked'
        })

    if len(additional_patients) >= 3:
        booked_appointments.append({
            'patient_id': additional_patients[2].id,
            'date': today + timedelta(days=6),
            'time': time(19, 0),
            'status': 'Booked'
        })

    # Create booked appointments
    for apt_data in booked_appointments:
        appointment = Appointment(
            patient_id=apt_data['patient_id'],
            doctor_id=demo_doctor_id,
            appointment_date=apt_data['date'],
            appointment_time=apt_data['time'],
            status=apt_data['status']
        )
        db.session.add(appointment)

    # 3. Cancelled appointments
    cancelled_appointments = [
        {
            'patient_id': demo_patient_id,
            'date': today - timedelta(days=2),
            'time': time(16, 0),
            'status': 'Cancelled',
            'reason': 'Patient had to travel urgently'
        }
    ]

    if len(additional_patients) >= 1:
        cancelled_appointments.append({
            'patient_id': additional_patients[0].id,
            'date': today - timedelta(days=1),
            'time': time(12, 0),
            'status': 'Cancelled',
            'reason': 'Patient rescheduled to a later date'
        })

    # Create cancelled appointments
    for apt_data in cancelled_appointments:
        appointment = Appointment(
            patient_id=apt_data['patient_id'],
            doctor_id=demo_doctor_id,
            appointment_date=apt_data['date'],
            appointment_time=apt_data['time'],
            status=apt_data['status']
        )
        appointment.cancellation_reason = apt_data['reason']
        db.session.add(appointment)


def cleanup_old_data():
    """
    Clean up old data
    - Remove past doctor availability slots
    - Archive old appointments (optional)
    """
    from models.doctor import DoctorAvailability

    try:
        # Remove past availability slots
        DoctorAvailability.remove_past_availability()
        print("[+] Cleaned up past availability slots")

    except Exception as e:
        print(f"[X] Error cleaning up data: {str(e)}")


def get_database_stats():
    """
    Get database statistics
    Returns dictionary with counts of various entities
    """
    from models.user import User
    from models.doctor import Doctor
    from models.patient import Patient
    from models.appointment import Appointment
    from models.treatment import Treatment

    stats = {
        'total_users': User.query.count(),
        'total_admins': User.query.filter_by(role='admin').count(),
        'total_doctors': Doctor.query.count(),
        'total_patients': Patient.query.count(),
        'total_specializations': Specialization.query.count(),
        'total_appointments': Appointment.query.count(),
        'booked_appointments': Appointment.query.filter_by(status='Booked').count(),
        'completed_appointments': Appointment.query.filter_by(status='Completed').count(),
        'cancelled_appointments': Appointment.query.filter_by(status='Cancelled').count(),
        'total_treatments': Treatment.query.count()
    }

    return stats


def print_database_stats():
    """Print database statistics"""
    stats = get_database_stats()

    print("\n" + "="*60)
    print("DATABASE STATISTICS")
    print("="*60)
    print(f"Total Users:              {stats['total_users']}")
    print(f"  - Admins:               {stats['total_admins']}")
    print(f"  - Doctors:              {stats['total_doctors']}")
    print(f"  - Patients:             {stats['total_patients']}")
    print(f"\nSpecializations:          {stats['total_specializations']}")
    print(f"\nAppointments:")
    print(f"  - Total:                {stats['total_appointments']}")
    print(f"  - Booked:               {stats['booked_appointments']}")
    print(f"  - Completed:            {stats['completed_appointments']}")
    print(f"  - Cancelled:            {stats['cancelled_appointments']}")
    print(f"\nTreatments:               {stats['total_treatments']}")
    print("="*60 + "\n")


def verify_admin_exists():
    """
    Verify that default admin user exists
    Returns True if exists, False otherwise
    """
    admin_user = User.query.filter_by(username='admin', role='admin').first()
    return admin_user is not None


def create_backup():
    """
    Create database backup (for SQLite)
    Copies the database file with timestamp
    """
    import shutil
    from datetime import datetime
    import os

    try:
        db_path = 'instance/hospital.db'
        if not os.path.exists(db_path):
            print("[X] Database file not found!")
            return False

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f'instance/hospital_backup_{timestamp}.db'

        shutil.copy2(db_path, backup_path)
        print(f"[+] Database backup created: {backup_path}")
        return True

    except Exception as e:
        print(f"[X] Error creating backup: {str(e)}")
        return False
