"""Database connection and query helper utilities."""

import mysql.connector
from mysql.connector import Error
from models.logger import Logger

class DatabaseConnectionError(Exception):
    """Raised when establishing a DB connection fails."""
    pass


class DatabaseConnection:
    """Thin wrapper around mysql-connector with logging support."""

    def __init__(self, host="localhost", user="python_user", password="MyPassw0rd!", database="product_db"):
        """Initialize connection configuration and logger."""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.logger = Logger()

    def connect(self):
        """Establish and return a MySQL connection."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                self.logger.write_log("DB_CONNECT", "Database connected successfully")
                return self.connection
        except Error as e:
            self.logger.write_log("DB_ERROR", f"Database connection failed: {str(e)}")
            raise DatabaseConnectionError("Failed to connect to database") from e

    def disconnect(self):
        """Close active database connection if present."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.logger.write_log("DB_DISCONNECT", "Database connection closed")

    def execute_query(self, query, params=None):
        """Execute INSERT/UPDATE/DELETE query and commit transaction."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            self.logger.write_log("DB_QUERY", f"Executed query: {query}")
        except Error as e:
            self.logger.write_log("DB_ERROR", f"Query execution failed: {str(e)}")
            raise

    def fetch_data(self, query, params=None):
        """Execute SELECT query and return rows as dictionaries."""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            result = cursor.fetchall()
            self.logger.write_log("DB_QUERY", f"Fetched data with query: {query}")
            return result
        except Error as e:
            self.logger.write_log("DB_ERROR", f"Fetch failed: {str(e)}")
            raise
