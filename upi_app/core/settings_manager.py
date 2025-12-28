from .database import DatabaseManager

class SettingsManager:
    def __init__(self):
        self.db = DatabaseManager()

    def get_setting(self, key, default=None):
        row = self.db.fetch_one("SELECT value FROM settings WHERE key = ?", (key,))
        return row['value'] if row else default

    def set_setting(self, key, value):
        self.db.execute("""
            INSERT INTO settings (key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value=excluded.value
        """, (key, value))

    @property
    def default_save_dir(self):
        return self.get_setting("default_save_dir")
    
    @default_save_dir.setter
    def default_save_dir(self, value):
        self.set_setting("default_save_dir", value)

    @property
    def theme(self):
        return self.get_setting("theme", "System")
    
    @theme.setter
    def theme(self, value):
        self.set_setting("theme", value)

    @property
    def default_vpa(self):
        return self.get_setting("default_vpa", "")

    @default_vpa.setter
    def default_vpa(self, value):
        self.set_setting("default_vpa", value)

    @property
    def default_name(self):
        return self.get_setting("default_name", "")

    @default_name.setter
    def default_name(self, value):
        self.set_setting("default_name", value)
