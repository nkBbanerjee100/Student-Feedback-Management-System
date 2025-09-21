from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.student import Student

student_bp = Blueprint("student", __name__)

# Student registration
@student_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        student = Student(name=name, email=email, password=password)
        if student.register():
            flash("Registration successful. Please login.", "success")
            return redirect(url_for("student.login"))
        else:
            flash("Registration failed. Email may already exist.", "danger")
    return render_template("register.html")


# Student login
@student_bp.route("/login", methods=["GET", "POST"])
def login():
    error_msg = None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        student = Student(email=email, password=password)
        success,msg = student.login()
        if success:
            session["student_email"] = email
            flash(msg, "success")
            return redirect(url_for("student.dashboard"))
        else:
            flash("Invalid email or password", "danger")
            error_msg = msg
            print("Login Failed for :",email)
    return render_template("login.html",error_msg = error_msg)


@student_bp.route("/logout")
def logout():
    session.pop("student_email", None)  # Remove session key
    flash("Logged out successfully.", "success")
    return redirect(url_for("home"))  # Redirect to homepage


# Example student dashboard
@student_bp.route("/dashboard")
def dashboard():
    if "student_email" not in session:
        return redirect(url_for("student.login"))
    return f"Welcome {session['student_email']}! (Dashboard page coming soon)"
