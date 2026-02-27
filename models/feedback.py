"""Feedback domain model for course-review submission logic."""

from models.database import DatabaseConnection
from models.logger import Logger
import datetime


class Feedback:
    """Represents a single feedback submission attempt."""

    def __init__(self, student_email, course_id, rating, comments):
        """Create feedback object from request payload values."""
        self.student_email = student_email
        self.course_id = course_id
        self.rating = rating
        self.comments = comments
        self.logger = Logger()

    def submit(self):
        """Insert feedback unless same student already reviewed the course."""
        db = DatabaseConnection()
        try:
            conn = db.connect()

            # Duplicate guard: one review per student per course.
            query_check = "SELECT * FROM feedback WHERE student_email=%s AND course_id=%s"
            existing = db.fetch_data(query_check, (self.student_email, self.course_id))

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if existing and len(existing) > 0:
                self.logger.write_log(
                    "FEEDBACK",
                    f"Duplicate feedback attempt by {self.student_email} for course_id {self.course_id} at {timestamp}"
                )
                return False, "You have already submitted review for this course."

            query_insert = """
                INSERT INTO feedback (student_email, course_id, rating, comments)
                VALUES (%s,%s,%s,%s)
            """
            db.execute_query(query_insert, (self.student_email, self.course_id, self.rating, self.comments))

            self.logger.write_log(
                "FEEDBACK",
                f"Feedback submitted by {self.student_email} for course_id {self.course_id} at {timestamp} | Rating: {self.rating} | Comment: {self.comments}"
            )

            return True, "Feedback submitted successfully!"

        except Exception as e:
            self.logger.write_log(
                "FEEDBACK_ERROR",
                f"Error submitting feedback by {self.student_email} for course_id {self.course_id} at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Error: {str(e)}"
            )
            print("Error submitting feedback:", e)
            return False, "Error submitting feedback."
        finally:
            db.disconnect()
