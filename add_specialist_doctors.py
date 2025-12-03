"""
Script to add specialist doctors to the database
Run this to add the 5 specialist demo doctors
"""

from app import create_app
from extensions import db, bcrypt
from utils.database import create_specialist_doctors

if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        print("=" * 50)
        print("Adding Specialist Doctors to Database")
        print("=" * 50)

        create_specialist_doctors(db, bcrypt)

        print("\n" + "=" * 50)
        print("Done!")
        print("=" * 50)
