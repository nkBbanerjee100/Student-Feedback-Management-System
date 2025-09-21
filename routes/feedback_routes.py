from flask import Blueprint, render_template, request, redirect, url_for, session
from models.feedback import Feedback
from models.database import DatabaseConnection
from utils.auth_utils import student_login_required

feedback_bp = Blueprint("feedback", __name__)

@feedback_bp.route("/submit_feedback", methods=["GET", "POST"])
@student_login_required
def submit_feedback():
    if "student_email" not in session:
        return redirect(url_for("student.login"))

    db = DatabaseConnection()
    courses = []
    reviewed_course_ids = []
    try:
        conn = db.connect()
        # Get all courses
        courses = db.fetch_data("SELECT id, name FROM courses")
        # Get courses already reviewed by this student
        reviewed = db.fetch_data(
            "SELECT course_id FROM feedback WHERE student_email=%s",
            (session["student_email"],)
        )
        reviewed_course_ids = [r['course_id'] for r in reviewed]
    finally:
        db.disconnect()

    error_msg = None

    if request.method == "POST":
        course_id = int(request.form.get("course_id"))
        rating = int(request.form.get("rating"))
        comments = request.form.get("comments")

        feedback = Feedback(session["student_email"], course_id, rating, comments)
        success, msg = feedback.submit()

        if not success:
            error_msg = msg
        else:
            return redirect(url_for("student.dashboard"))

    return render_template(
        "submit_feedback.html",
        courses=courses,
        reviewed_course_ids=reviewed_course_ids,
        error_msg=error_msg
    )
