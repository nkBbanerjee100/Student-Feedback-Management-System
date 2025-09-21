import mysql.connector
from mysql.connector import Error
from models.logger import Logger

# Custom exception class for DB errors
class DatabaseConnectionError(Exception):
    pass


class DatabaseConnection:
    def __init__(self, host="localhost", user="python_user", password="MyPassw0rd!", database="product_db"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.logger = Logger()

    def connect(self):
        """Establish connection to MySQL database"""
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
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.logger.write_log("DB_DISCONNECT", "Database connection closed")

    def execute_query(self, query, params=None):
        """Execute INSERT/UPDATE/DELETE query with exception handling"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            self.logger.write_log("DB_QUERY", f"Executed query: {query}")
        except Error as e:
            self.logger.write_log("DB_ERROR", f"Query execution failed: {str(e)}")
            raise

    def fetch_data(self, query, params=None):
        """Execute SELECT query and return results"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            result = cursor.fetchall()
            self.logger.write_log("DB_QUERY", f"Fetched data with query: {query}")
            return result
        except Error as e:
            self.logger.write_log("DB_ERROR", f"Fetch failed: {str(e)}")
            raise
