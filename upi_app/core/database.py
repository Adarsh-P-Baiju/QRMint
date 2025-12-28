import sqlite3
import os
from datetime import datetime

DB_FILE = "upi_app.db"

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.init_db()
        return cls._instance

    def init_db(self):
        self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                vpa TEXT,
                name TEXT,
                amount TEXT,
                note TEXT,
                source TEXT,
                batch_id TEXT,
                paid_status TEXT,
                file_path TEXT
            )
        """)
        
        cursor.execute("PRAGMA table_info(history)")
        columns = [info[1] for info in cursor.fetchall()]
        if "file_path" not in columns:
            cursor.execute("ALTER TABLE history ADD COLUMN file_path TEXT")
        
        cursor.execute("PRAGMA table_info(history)")
        columns = [info[1] for info in cursor.fetchall()]
        if "paid_status" not in columns:
            cursor.execute("ALTER TABLE history ADD COLUMN paid_status TEXT DEFAULT 'Unpaid'")

        if "logo_path" not in columns:
            cursor.execute("ALTER TABLE history ADD COLUMN logo_path TEXT")
        
        cursor.execute("PRAGMA table_info(history)")
        columns = [info[1] for info in cursor.fetchall()]
        if "fg_color" not in columns:
            cursor.execute("ALTER TABLE history ADD COLUMN fg_color TEXT DEFAULT 'black'")
        if "bg_color" not in columns:
            cursor.execute("ALTER TABLE history ADD COLUMN bg_color TEXT DEFAULT 'white'")
        
        cursor.execute("PRAGMA table_info(history)")
        columns = [info[1] for info in cursor.fetchall()]
        if "qr_style" not in columns:
            cursor.execute("ALTER TABLE history ADD COLUMN qr_style TEXT DEFAULT 'square'")
        if "frame_text" not in columns:
            cursor.execute("ALTER TABLE history ADD COLUMN frame_text TEXT")
        if "logo_mask" not in columns:
            cursor.execute("ALTER TABLE history ADD COLUMN logo_mask TEXT DEFAULT 'square'")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS templates (
                id TEXT PRIMARY KEY,
                name TEXT,
                vpa TEXT,
                amount TEXT,
                note TEXT
            )
        """)
        
        cursor.execute("PRAGMA table_info(templates)")
        columns = [info[1] for info in cursor.fetchall()]
        if "fg_color" not in columns:
            cursor.execute("ALTER TABLE templates ADD COLUMN fg_color TEXT DEFAULT 'black'")
        if "bg_color" not in columns:
            cursor.execute("ALTER TABLE templates ADD COLUMN bg_color TEXT DEFAULT 'white'")
        if "qr_style" not in columns:
            cursor.execute("ALTER TABLE templates ADD COLUMN qr_style TEXT DEFAULT 'square'")
        if "frame_text" not in columns:
            cursor.execute("ALTER TABLE templates ADD COLUMN frame_text TEXT")
        if "logo_mask" not in columns:
            cursor.execute("ALTER TABLE templates ADD COLUMN logo_mask TEXT DEFAULT 'square'")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bank_accounts (
                id TEXT PRIMARY KEY,
                bank_name TEXT,
                vpa TEXT,
                account_holder TEXT,
                is_default INTEGER DEFAULT 0,
                created_at TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        
        self.conn.commit()

    def execute(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor

    def fetch_all(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def fetch_one(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None
