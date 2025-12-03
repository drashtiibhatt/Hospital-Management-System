# Setup Guide

## Prerequisites

Before setting up the Hospital Management System, ensure you have the following installed:

- **Python 3.8 or higher**
- **pip** (Python package manager)
- **Git** (optional, for version control)
- **Text Editor/IDE** (VS Code, PyCharm, etc.)

---

## Installation Steps

### Step 1: Create Project Directory

```bash
mkdir hospital_management_system
cd hospital_management_system
```

---

### Step 2: Set Up Virtual Environment

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

You should see `(venv)` prefix in your terminal after activation.

---

### Step 3: Install Required Packages

Create `requirements.txt` file with the following content:

```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-Bcrypt==1.0.1
Flask-WTF==1.2.1
WTForms==3.1.1
email-validator==2.1.0
```

Install packages:
```bash
pip install -r requirements.txt
```

---

### Step 4: Create Configuration File

Create `config.py` in the root directory:

```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/hospital.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
```

---

### Step 5: Create Folder Structure

```bash
# Create all necessary folders
mkdir models controllers api templates static utils docs instance

# Create subdirectories
mkdir templates/admin templates/doctor templates/patient
mkdir static/css static/js static/images
```

---

### Step 6: Initialize Database

The database will be created automatically when you run the application for the first time. The `init_db()` function in `utils/database.py` handles:
- Table creation
- Default admin user creation
- Sample specialization data

**Default Admin Credentials:**
```
Username: admin
Password: admin123
Email: admin@hospital.com
```

---

### Step 7: Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000/`

---

## Verification Steps

### 1. Check Database Creation

After running the app, verify that `instance/hospital.db` file is created.

### 2. Test Admin Login

1. Navigate to `http://127.0.0.1:5000/login`
2. Login with:
   - Username: `admin`
   - Password: `admin123`
3. You should be redirected to the admin dashboard

### 3. Check Routes

Test the following routes:
- `/` - Landing page
- `/login` - Login page
- `/register` - Patient registration
- `/admin/dashboard` - Admin dashboard (requires admin login)
- `/doctor/dashboard` - Doctor dashboard (requires doctor login)
- `/patient/dashboard` - Patient dashboard (requires patient login)

---

## Common Issues & Troubleshooting

### Issue 1: Module Not Found Error

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
# Ensure virtual environment is activated
# Then reinstall packages
pip install -r requirements.txt
```

---

### Issue 2: Database Not Created

**Error:** Database file not found

**Solution:**
```bash
# Manually create instance directory
mkdir instance

# Then run the app
python app.py
```

---

### Issue 3: Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Run on a different port
python app.py --port 5001
```

Or modify `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)
```

---

### Issue 4: Template Not Found

**Error:** `jinja2.exceptions.TemplateNotFound`

**Solution:**
- Ensure templates are in the `templates/` directory
- Check the template path in `render_template()`

---

### Issue 5: Static Files Not Loading

**Solution:**
- Clear browser cache
- Check the path in templates: `{{ url_for('static', filename='css/style.css') }}`
- Ensure files are in the correct `static/` subdirectory

---

## Development Mode

### Enable Debug Mode

In `app.py`:
```python
app.run(debug=True)
```

**Benefits:**
- Auto-reload on code changes
- Detailed error messages
- Interactive debugger

**Warning:** Never enable debug mode in production!

---

## Database Reset

To reset the database (delete all data):

```bash
# Stop the application
# Delete the database file
rm instance/hospital.db

# On Windows:
del instance\hospital.db

# Run the app again to recreate
python app.py
```

---

## Optional: REST API Setup

If implementing REST APIs, install:

```bash
pip install Flask-RESTful==0.3.10
```

Update `requirements.txt` accordingly.

---

## Environment Variables (Production)

For production deployment, set environment variables:

**Windows:**
```bash
set FLASK_ENV=production
set SECRET_KEY=your-super-secret-key-here
```

**macOS/Linux:**
```bash
export FLASK_ENV=production
export SECRET_KEY=your-super-secret-key-here
```

---

## Running Tests

(To be implemented later)

```bash
# Install pytest
pip install pytest

# Run tests
pytest tests/
```

---

## Deployment (Basic)

### Using Gunicorn (Linux/macOS):

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Using Waitress (Windows):

```bash
pip install waitress
waitress-serve --host 0.0.0.0 --port 8000 app:app
```

---

## Project Dependencies

After installation, verify with:

```bash
pip list
```

Expected packages:
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Bcrypt
- Flask-WTF
- WTForms
- email-validator

---

## Next Steps

1. ✅ Complete database model implementation
2. ✅ Implement authentication system
3. ✅ Build admin module
4. ✅ Build doctor module
5. ✅ Build patient module
6. ✅ Add validation and error handling
7. ✅ Style with Bootstrap
8. ✅ Test all functionalities

---

## Useful Commands

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Deactivate virtual environment
deactivate

# Install new package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Run the app
python app.py

# Check Python version
python --version
```

---

## Resources

- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
- Bootstrap Documentation: https://getbootstrap.com/docs/

---

**Last Updated:** 2025-11-26
