from flask import Flask, jsonify

# Create a Flask application instance
app = Flask(__name__)

# Define a simple route to handle HTTP GET requests
@app.route('/')
def home():
    """
    This function handles the root route ('/') and returns a JSON response.
    The JSON response includes a message indicating the app is running on Vercel.
    """
    return jsonify(message="Hello from Flask on Vercel!")

# Vercel serverless functions use this entry point to invoke the application.
# The 'app' variable is recognized by Vercel as the application to handle incoming requests.
# No need for app.run() as Vercel automatically handles the function execution.
