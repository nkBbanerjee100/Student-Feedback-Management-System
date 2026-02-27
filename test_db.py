"""Manual DB connectivity smoke test utility.

Run directly to validate DB connection and basic SELECT operations.
"""

from models.database import DatabaseConnection

if __name__ == "__main__":
    """Open a DB connection, run a sample query, and close connection."""
    db = DatabaseConnection(user="python_user", password="MyPassw0rd!", database="product_db")
    try:
        conn = db.connect()

        # Example fetch query for quick verification.
        rows = db.fetch_data("SELECT * FROM student")
        print(rows)
    finally:
        db.disconnect()
