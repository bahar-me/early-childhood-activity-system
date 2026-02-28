from backend.database import get_db_connection


def init_db():
    with get_db_connection() as connection:

        # Users tablosunu oluştur
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'teacher'
                    CHECK(role IN ('teacher', 'admin'))
            )
        """)

        # Refresh token tablosunu oluştur
        connection.execute("""
            CREATE TABLE IF NOT EXISTS refresh_tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token TEXT NOT NULL,
                expires_at DATETIME NOT NULL,
                is_revoked BOOLEAN DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id) 
            )
        """)
        connection.commit()
    
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()