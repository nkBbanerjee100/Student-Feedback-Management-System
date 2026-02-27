"""Application entrypoint for the Student Feedback Management System.

Creates and configures the Flask app, registers blueprints, and exposes
the root landing page.
"""

from flask import Flask, render_template
import os
from dotenv import load_dotenv
from datetime import timedelta
from routes.student_routes import student_bp
from routes.feedback_routes import feedback_bp
from routes.admin_routes import admin_bp

# Load environment variables from .env in project root.
load_dotenv()

app = Flask(__name__)

# Session configuration.
app.secret_key = os.getenv("SECRET_KEY", "fallback_key")
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home():
    """Render the landing page with student/admin navigation."""
    return render_template("base.html")

# Register feature blueprints under dedicated URL prefixes.
app.register_blueprint(student_bp, url_prefix="/student")
app.register_blueprint(feedback_bp, url_prefix="/feedback")
app.register_blueprint(admin_bp, url_prefix="/admin")

# Print route table at startup for quick debugging.
print("\nAvailable Routes:")
for rule in app.url_map.iter_rules():
    print(f"{rule} -> {rule.endpoint}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
