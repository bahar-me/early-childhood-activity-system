from multiprocessing.dummy import connection

from backend.database import get_db_connection


def init_db():
    with get_db_connection() as connection:

        # Schools tablosu
        connection.execute("""
            CREATE TABLE IF NOT EXISTS schools (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Users tablosunu oluştur
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'teacher'
                    CHECK(role IN ('teacher', 'school_admin', system_admin')),
                school_id INTEGER,
                FOREIGN KEY (school_id) REFERENCES schools (id)
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

# Test için örnek bir okul ekleyelim
connection.execute("""
    INSERT INTO schools (name, address)
    VALUES ('Test School', 'Istanbul')
""")
connection.commit()

if __name__ == "__main__":
    init_db()