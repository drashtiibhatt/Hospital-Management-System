# vercel_entry.py

from app import create_app

# Create the Flask app instance
app = create_app(config_name="production")  # Or "development" based on your environment
