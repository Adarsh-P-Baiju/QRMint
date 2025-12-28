from datetime import datetime
from .database import DatabaseManager

class BankManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def add_bank(self, bank_name, vpa, account_holder, is_default=False):
        """Add a new bank account"""
        bank_id = datetime.now().strftime('%Y%m%d%H%M%S%f')
        created_at = datetime.now().isoformat()
        
        if is_default:
            self.db.execute("UPDATE bank_accounts SET is_default = 0")
        
        self.db.execute("""
            INSERT INTO bank_accounts (id, bank_name, vpa, account_holder, is_default, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (bank_id, bank_name, vpa, account_holder, 1 if is_default else 0, created_at))
        
        return bank_id
    
    def update_bank(self, bank_id, bank_name, vpa, account_holder, is_default=None):
        """Update an existing bank account"""
        if is_default:
            self.db.execute("UPDATE bank_accounts SET is_default = 0")
        
        if is_default is not None:
            self.db.execute("""
                UPDATE bank_accounts 
                SET bank_name = ?, vpa = ?, account_holder = ?, is_default = ?
                WHERE id = ?
            """, (bank_name, vpa, account_holder, 1 if is_default else 0, bank_id))
        else:
            self.db.execute("""
                UPDATE bank_accounts 
                SET bank_name = ?, vpa = ?, account_holder = ?
                WHERE id = ?
            """, (bank_name, vpa, account_holder, bank_id))
    
    def delete_bank(self, bank_id):
        """Delete a bank account"""
        self.db.execute("DELETE FROM bank_accounts WHERE id = ?", (bank_id,))
    
    def get_all_banks(self):
        """Get all bank accounts"""
        return self.db.fetch_all("SELECT * FROM bank_accounts ORDER BY is_default DESC, bank_name ASC")
    
    def get_default_bank(self):
        """Get the default bank account"""
        return self.db.fetch_one("SELECT * FROM bank_accounts WHERE is_default = 1")
    
    def set_default_bank(self, bank_id):
        """Set a bank as default"""
        self.db.execute("UPDATE bank_accounts SET is_default = 0")
        self.db.execute("UPDATE bank_accounts SET is_default = 1 WHERE id = ?", (bank_id,))
