from models.database import DatabaseConnection
from models.logger import Logger
from mysql.connector import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask import current_app

class Admin:
    def __init__(self, admin_id=None, name="", email="", password=""):
        self.admin_id = admin_id
        self.name = name
        self.email = email
        self.password = password
        self.db = DatabaseConnection()
        log_path = os.path.join(current_app.root_path, "logs", "app.log")
        self.logger = Logger(logfile=log_path)

    def register(self):
        """Register a new admin with hashed password"""
        try:
            conn = self.db.connect()
            hashed_password = generate_password_hash(self.password)  # Hash password
            query = "INSERT INTO admins (name, email, password) VALUES (%s, %s, %s)"
            self.db.execute_query(query, (self.name, self.email, hashed_password))
            self.logger.write_log("ADMIN_REGISTER", f"Admin {self.email} registered successfully")
            return True, "Admin registered successfully"
        except IntegrityError:
            self.logger.write_log("ADMIN_REGISTER_FAIL", f"Duplicate email: {self.email}")
            return False, "Email already registered"
        except Exception as e:
            self.logger.write_log("ADMIN_REGISTER_FAIL", f"Error: {str(e)}")
            return False, f"Registration failed: {str(e)}"
        finally:
            try:
                self.db.disconnect()
            except Exception as e:
                self.logger.write_log("DB_DISCONNECT_FAIL", f"Error disconnecting DB: {str(e)}")

    def login(self):
        """Validate admin login with hashed password"""
        try:
            conn = self.db.connect()
            query = "SELECT * FROM admins WHERE email=%s"
            result = self.db.fetch_data(query, (self.email,))
            if result:
                stored_hash = result[0]["password"]
                if check_password_hash(stored_hash, self.password):
                    self.logger.write_log("ADMIN_LOGIN", f"Admin {self.email} logged in successfully")
                    return True, "Login successful"
            self.logger.write_log("ADMIN_LOGIN_FAIL", f"Invalid credentials for {self.email}")
            return False, "Invalid email or password"
        except Exception as e:
            self.logger.write_log("ADMIN_LOGIN_FAIL", f"Error: {str(e)}")
            return False, f"Login failed: {str(e)}"
        finally:
            try:
                self.db.disconnect()
            except Exception as e:
                self.logger.write_log("DB_DISCONNECT_FAIL", f"Error disconnecting DB: {str(e)}")

    def dashboard(self):
        """Fetch all feedback with course names as dictionaries"""
        try:
            conn = self.db.connect()
            query = """
                SELECT f.id, f.student_email, c.name AS course_name, f.rating, f.comments, f.submitted_at
                FROM feedback f
                JOIN courses c ON f.course_id = c.id
                ORDER BY f.submitted_at DESC
            """
            # Ensure dictionary=True in cursor
            result = self.db.fetch_data(query)
            # Convert tuples to dicts if needed
            feedback_list = []
            for row in result:
                if isinstance(row, dict):
                    feedback_list.append(row)
                else:
                    # fallback for tuple
                    feedback_list.append({
                        "id": row[0],
                        "student_email": row[1],
                        "course_name": row[2],
                        "rating": row[3],
                        "comments": row[4],
                        "submitted_at": row[5],
                    })
            return feedback_list
        except Exception as e:
            self.logger.write_log("FETCH_FEEDBACK_FAIL", f"Error: {str(e)}")
            return []
        finally:
            try:
                self.db.disconnect()
            except:
                pass
    
    