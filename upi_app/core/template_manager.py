import sqlite3

class TemplateManager:
    def __init__(self, db_path="upi_app.db"):
        self.db_path = db_path
        self._init_table()
        
    def _init_table(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS templates (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        vpa TEXT NOT NULL,
                        amount TEXT,
                        note TEXT
                    )
                """)
                conn.commit()
        except: pass

    def add_template(self, name, vpa, amount, note, fg_color="black", bg_color="white", qr_style="square", frame_text=None, logo_mask="square"):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""INSERT INTO templates (name, vpa, amount, note, fg_color, bg_color, qr_style, frame_text, logo_mask) 
                               VALUES (?,?,?,?,?,?,?,?,?)""", 
                             (name, vpa, amount, note, fg_color, bg_color, qr_style, frame_text, logo_mask))
                conn.commit()
            return True
        except: return False

    def get_templates(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM templates ORDER BY id DESC")
                return [dict(row) for row in cursor.fetchall()]
        except: return []

    def delete_template(self, tid):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM templates WHERE id=?", (tid,))
                conn.commit()
            return True
        except: return False
