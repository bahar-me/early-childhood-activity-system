from flask import Flask
from backend.api.auth.routes import auth_bp # Import the auth blueprint

app = Flask(__name__)

# Register the auth blueprint
app.register_blueprint(auth_bp, url_prefix="/api/auth")

@app.route("/")
def home():
    return "Backend is running"

if __name__ == "__main__":
    app.run(debug=True)
