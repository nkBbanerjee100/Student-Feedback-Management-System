from flask import Flask,render_template
import os
from dotenv import load_dotenv
from datetime import timedelta
from routes.student_routes import student_bp
from routes.feedback_routes import feedback_bp
from routes.admin_routes import admin_bp

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Set secret key for sessions
app.secret_key = os.getenv("SECRET_KEY", "fallback_key")
app.permanent_session_lifetime = timedelta(minutes=5)

# Home route
@app.route("/")
def home():
    return render_template("base.html")

# Register blueprints with proper URL prefixes
app.register_blueprint(student_bp, url_prefix="/student")      # all student routes under /student
app.register_blueprint(feedback_bp, url_prefix="/feedback")    # all feedback routes under /feedback
app.register_blueprint(admin_bp, url_prefix="/admin")          # all admin routes under /admin

# Print all URL rules for debugging
print("\nAvailable Routes:")
for rule in app.url_map.iter_rules():
    print(f"{rule} -> {rule.endpoint}")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0", port=port)
    
