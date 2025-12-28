from datetime import datetime
from .database import DatabaseManager

class HistoryManager:
    def __init__(self):
        self.db = DatabaseManager()

    def add_record(self, vpa, name, amount, note, source="Manual", batch_id=None, paid_status="Unpaid", file_path=None, logo_path=None, fg_color="black", bg_color="white", qr_style="square", frame_text=None, logo_mask="square"):
        record_id = datetime.now().strftime('%Y%m%d%H%M%S%f')
        timestamp = datetime.now().isoformat()
        
        
        self.db.execute("""
            INSERT INTO history (id, timestamp, vpa, name, amount, note, source, batch_id, paid_status, file_path, logo_path, fg_color, bg_color, qr_style, frame_text, logo_mask)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (record_id, timestamp, vpa, name, amount, note, source, batch_id, paid_status, file_path, logo_path, fg_color, bg_color, qr_style, frame_text, logo_mask))
        
        return {
            "id": record_id, "timestamp": timestamp,
            "vpa": vpa, "name": name, "amount": amount, "note": note,
            "source": source, "batch_id": batch_id, "paid_status": paid_status, "logo_path": logo_path,
            "fg_color": fg_color, "bg_color": bg_color, "qr_style": qr_style, "frame_text": frame_text, "logo_mask": logo_mask
        }

    def delete_record(self, record_id):
        self.db.execute("DELETE FROM history WHERE id = ?", (record_id,))

    def update_record(self, record_id, vpa, name, amount, note, paid_status, logo_path=None, fg_color=None, bg_color=None, qr_style=None, frame_text=None, logo_mask=None):
        self.db.execute("""
            UPDATE history 
            SET vpa = ?, name = ?, amount = ?, note = ?, paid_status = ?
            WHERE id = ?
        """, (vpa, name, amount, note, paid_status, record_id))
        
        if logo_path is not None:
             self.db.execute("UPDATE history SET logo_path = ? WHERE id = ?", (logo_path, record_id))
        
        if fg_color is not None:
             self.db.execute("UPDATE history SET fg_color = ? WHERE id = ?", (fg_color, record_id))
        if bg_color is not None:
             self.db.execute("UPDATE history SET bg_color = ? WHERE id = ?", (bg_color, record_id))
        
        if qr_style is not None:
             self.db.execute("UPDATE history SET qr_style = ? WHERE id = ?", (qr_style, record_id))
        if frame_text is not None:
             self.db.execute("UPDATE history SET frame_text = ? WHERE id = ?", (frame_text, record_id))
        if logo_mask is not None:
             self.db.execute("UPDATE history SET logo_mask = ? WHERE id = ?", (logo_mask, record_id))

    def get_stats(self):
        """
        Returns stats including paid/unpaid amounts and counts.
        """
        stats = {}
        
        row = self.db.fetch_one("SELECT COUNT(*) as cnt FROM history")
        stats['total_count'] = row['cnt'] if row else 0
        
        
        row = self.db.fetch_one("SELECT SUM(CAST(amount as REAL)) as total FROM history WHERE amount != ''")
        stats['total_amount'] = row['total'] if row and row['total'] else 0.0
        
        row = self.db.fetch_one("SELECT SUM(CAST(amount as REAL)) as total FROM history WHERE amount != '' AND paid_status = 'Paid'")
        stats['paid_amount'] = row['total'] if row and row['total'] else 0.0
        
        row = self.db.fetch_one("SELECT SUM(CAST(amount as REAL)) as total FROM history WHERE amount != '' AND paid_status = 'Unpaid'")
        stats['unpaid_amount'] = row['total'] if row and row['total'] else 0.0
        
        stats['paid_count'] = self.db.fetch_one("SELECT COUNT(*) as cnt FROM history WHERE paid_status = 'Paid'")['cnt']
        stats['unpaid_count'] = self.db.fetch_one("SELECT COUNT(*) as cnt FROM history WHERE paid_status = 'Unpaid'")['cnt']
        stats['pending_count'] = self.db.fetch_one("SELECT COUNT(*) as cnt FROM history WHERE paid_status = 'Pending'")['cnt']
        
        stats['batch_count'] = self.db.fetch_one("SELECT COUNT(*) as cnt FROM history WHERE source = 'Batch'")['cnt']
        stats['manual_count'] = self.db.fetch_one("SELECT COUNT(*) as cnt FROM history WHERE source = 'Manual'")['cnt']
        
        stats['recent_history'] = self.db.fetch_all("SELECT * FROM history ORDER BY timestamp DESC LIMIT 5")
        
        return stats

    def get_daily_trends(self, limit=30):
        """
        Returns daily sums for Total and Paid amounts.
        Ordered by date ascending.
        Limit None means all time.
        """
        limit_clause = f"LIMIT {limit}" if limit else ""
        
        query = f"""
            SELECT 
                date(timestamp) as day, 
                SUM(CAST(amount as REAL)) as total_vol,
                SUM(CASE WHEN paid_status='Paid' THEN CAST(amount as REAL) ELSE 0 END) as paid_vol
            FROM history
            WHERE amount != ''
            GROUP BY day
            ORDER BY day DESC
            {limit_clause}
        """
        
        rows = self.db.fetch_all(query)
        rows.reverse()
        return rows

    def get_all(self):
        return self.db.fetch_all("SELECT * FROM history ORDER BY timestamp DESC")

    def clear_history(self):
        self.db.execute("DELETE FROM history")

    def get_grouped_by_context(self):
        """
        Returns a dictionary grouping items by 'source' and 'batch_id' 
        """
        history = self.get_all()
        groups = {}
        
        for item in history:
            key = item.get("batch_id") if item.get("source") == "Batch" else "Individual"
            if not key: key = "Individual"
            
            if key not in groups:
                 groups[key] = []
            groups[key].append(item)
            
        return groups
