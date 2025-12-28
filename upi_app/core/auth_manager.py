import hashlib
import sqlite3
import os

class AuthManager:
    def __init__(self, db_path="upi_app.db"):
        self.db_path = db_path
        self._init_table()
        
    def _init_table(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS settings (
                        key TEXT PRIMARY KEY,
                        value TEXT
                    )
                """)
                conn.commit()
        except Exception as e:
            print(f"Auth Init Error: {e}")

    def is_setup_completed(self):
        return self.get_hash() is not None

    def get_hash(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT value FROM settings WHERE key='admin_password'")
                res = cursor.fetchone()
                return res[0] if res else None
        except: return None

    def set_password(self, password):
        hashed = hashlib.sha256(password.encode()).hexdigest()
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('admin_password', ?)", (hashed,))
                conn.commit()
            return True
        except Exception as e:
            print(f"Set Password Error: {e}")
            return False

    def verify_password(self, password):
        stored = self.get_hash()
        if not stored: return False
        hashed = hashlib.sha256(password.encode()).hexdigest()
        return stored == hashed
