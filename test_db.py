from models.database import DatabaseConnection

if __name__ == "__main__":
    db = DatabaseConnection(user="python_user", password="MyPassw0rd!", database="product_db")
    try:
        conn = db.connect()
        
        # Test insert
        # db.execute_query( "INSERT INTO student (name, email, password) VALUES (%s, %s, %s)", ("Test Student", "test@example.com", "12345") )
        
        # Test fetch
        rows = db.fetch_data("SELECT * FROM student")
        print(rows)
    finally:
        db.disconnect()
