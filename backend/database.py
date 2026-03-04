import sqlite3
from backend.config import DATABASE_URL

def get_db_connection():
    """
    Creates and returns a new database connection.
    """
    # SQLite URL'den dosya yolunu çıkar
    if DATABASE_URL.startswith("sqlite:///"):
        db_file = DATABASE_URL.replace("sqlite:///", "")
    else:
        raise ValueError("Unsupported database URL format")
    
    connection = sqlite3.connect(
        db_file,
        check_same_thread=False #Flask compatibility
        )
    
    connection.row_factory = sqlite3.Row
    return connection