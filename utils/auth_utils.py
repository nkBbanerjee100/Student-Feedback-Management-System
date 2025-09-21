from flask import session, redirect, url_for, flash
from functools import wraps

# Decorator to protect student routes
def student_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "student_email" not in session:
            flash("Please login as student first!", "warning")
            return redirect(url_for("student.login"))
        return f(*args, **kwargs)
    return decorated_function

# Decorator to protect admin routes
def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_email" not in session:
            flash("Please login as admin first!", "warning")
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated_function
