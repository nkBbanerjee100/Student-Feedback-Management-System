"""Student domain model for registration, login, and dashboard access."""

from models.database import DatabaseConnection
from models.logger import Logger
from mysql.connector import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash


class Student:
    """Represents a student and student-facing account operations."""

    def __init__(self, student_id=None, name="", email="", password=""):
        """Create a student model instance with persistence dependencies."""
        self.student_id = student_id
        self.name = name
        self.email = email
        self.password = password
        self.db = DatabaseConnection()
        self.logger = Logger()

    def register(self):
        """Register a new student with hashed password storage."""
        try:
            conn = self.db.connect()
            print("db connected")
            hashed_password = generate_password_hash(self.password) 
            query = "INSERT INTO student(name, email, password) VALUES (%s, %s, %s)"
            self.db.execute_query(query, (self.name, self.email, hashed_password))
            print("student inserted successfully")
            self.logger.write_log("REGISTER", f"Student {self.email} registered successfully")

            return True, "Registered successfully"
        except IntegrityError:
            self.logger.write_log("REGISTER_FAIL", f"Duplicate email: {self.email}")
            return False, "Email already registered"
        except Exception as e:
            self.logger.write_log("REGISTER_FAIL", f"Error: {str(e)}")
            return False, f"Registration failed: {str(e)}"
        finally:
            try:
                self.db.disconnect()
            except Exception as e:
                self.logger.write_log("DB_DISCONNECT_FAIL", f"Error disconnecting DB: {str(e)}")
    
    def login(self):
        """Validate student credentials using secure hash verification."""
        try:
            conn = self.db.connect()
            query = "SELECT * FROM student WHERE email=%s "
            result = self.db.fetch_data(query, (self.email,))
            if result:
                stored_hash = result[0]["password"]
                print("Stored hash:", stored_hash)
                print("Entered password (plain):", self.password)
                print("Password check:", check_password_hash(stored_hash, self.password))

                if check_password_hash(stored_hash, self.password):
                    print("success")
                    self.logger.write_log("LOGIN", f"Student {self.email} logged in successfully")
                    return True, "Login successful"
                else:
                    print("fail")
                    self.logger.write_log("LOGIN_FAIL", f"Wrong password for {self.email}")
                    return False, "Invalid email or password"
            else:
                self.logger.write_log("LOGIN_FAIL", f"Invalid credentials for {self.email}")
                return False, "Invalid email or password"
        except Exception as e:
            self.logger.write_log("LOGIN_FAIL", f"Error: {str(e)}")
            return False, f"Login failed: {str(e)}"
        finally:
            try:
                self.db.disconnect()
            except Exception as e:
                self.logger.write_log("DB_DISCONNECT_FAIL", f"Error disconnecting DB: {str(e)}")

    def dashboard(self):
        """Fetch and return basic profile details for dashboard context."""
        try:
            # Example: fetch student-specific info
            conn = self.db.connect()
            query = "SELECT id, name, email FROM student WHERE email=%s"
            student_info = self.db.fetch_data(query, (self.email,))
            if student_info:
                return True, student_info
            else:
                return False, "Student not found"
        except Exception as e:
            self.logger.write_log("DASHBOARD_FAIL", f"Error: {str(e)}")
            return False, f"Failed to load dashboard: {str(e)}"
        finally:
            try:
                self.db.disconnect()
            except Exception as e:
                self.logger.write_log("DB_DISCONNECT_FAIL", f"Error disconnecting DB: {str(e)}")
