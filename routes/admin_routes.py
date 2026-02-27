"""Admin-facing routes for account access, feedback view, and log access."""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file
from models.admin import Admin
from utils.files_utils import FUtils
from utils.auth_utils import admin_login_required
import os

admin_bp = Blueprint("admin", __name__)
LOG_FILE_PATH = os.path.join(os.getcwd(), "app.log")

@admin_bp.route("/register", methods=["GET", "POST"])
def register():
    """Handle admin registration form display and submission."""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        admin = Admin(name=name, email=email, password=password)

        success, msg = admin.register()
        if success:
            flash(msg, "success")
            return redirect(url_for("admin.login"))
        else:
            flash(msg, "danger")

    return render_template("admin_register.html")

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    """Authenticate admin credentials and create admin session."""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        admin = Admin(email=email, password=password)
        
        success, msg = admin.login()
        if success:
            session.permanent = True
            session["admin_email"] = email
            flash(msg, "success")
            return redirect(url_for("admin.view_feedback"))
        else:
            flash(msg, "danger")
    return render_template("admin_login.html")

@admin_bp.route("/view_feedback")
@admin_login_required
def view_feedback():
    """Render admin dashboard with all submitted feedback."""
    print("Accessing admin/view_feedback")
    if "admin_email" not in session:
        print("Admin not logged in!")
        flash("Please login as admin first!", "warning")
        return redirect(url_for("admin.login"))

    admin = Admin()
    feedback_list = admin.dashboard()
    return render_template("admin_view_feedback.html", feedback_list=feedback_list)

@admin_bp.route("/logs")
@admin_login_required
def view_logs():
    """Show application logs in browser for authenticated admins."""
    if "admin_email" not in session:
        return redirect(url_for("admin.login"))

    log_path = FUtils.get_log_file_path()
    logs = []

    if os.path.exists(log_path):
        print(f"Log file exists at {log_path}")
        with open(log_path, "r") as f:
            logs = f.readlines()
    else:
        print(f"Log file does not exist at {log_path}")
        logs = ["Log file does not exist."]

    return render_template("view_logs.html", logs=logs)


@admin_bp.route("/download_logs")
@admin_login_required
def download_logs():
    """Download current application log file as attachment."""
    if "admin_email" not in session:
        flash("Please login as admin", "warning")
        return redirect(url_for("admin.login"))

    log_path = FUtils.get_log_file_path()
    if os.path.exists(log_path):
        print(f"Sending log file from {log_path}")
        return send_file(log_path, as_attachment=True)
    else:
        print(f"Log file not found at {log_path}")
        flash("Log file not found.", "danger")
        return redirect(url_for("admin.view_logs"))


@admin_bp.route("/logout")
def logout():
    """Clear admin session and redirect to home page."""
    session.pop("admin_email", None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("home"))
