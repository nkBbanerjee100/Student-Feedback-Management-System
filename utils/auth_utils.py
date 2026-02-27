"""Authentication/authorization decorators for route protection."""

from flask import session, redirect, url_for, flash
from functools import wraps

def student_login_required(f):
    """Require student session before allowing route access."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "student_email" not in session:
            flash("Please login as student first!", "warning")
            return redirect(url_for("student.login"))
        return f(*args, **kwargs)
    return decorated_function


def admin_login_required(f):
    """Require admin session before allowing route access."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_email" not in session:
            flash("Please login as admin first!", "warning")
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated_function
