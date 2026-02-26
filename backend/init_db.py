from backend.database import get_db_connection


def init_db():
    with get_db_connection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'teacher'
                    CHECK(role IN ('teacher', 'admin'))
            )
        """)

        connection.commit()
    
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()