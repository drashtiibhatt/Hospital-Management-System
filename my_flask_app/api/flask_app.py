from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Hello from Flask on Vercel!")

# Vercel requires this to be named 'app'
if __name__ == "__main__":
    app.run(debug=True)
