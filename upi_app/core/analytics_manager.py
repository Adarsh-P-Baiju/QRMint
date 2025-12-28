import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict

class AnalyticsManager:
    def __init__(self, db_path="upi_app.db"):
        self.db_path = db_path
        
    def get_status_counts(self):
        """Return { 'Paid': 10, 'Unpaid': 5, ... }"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT paid_status, COUNT(*) FROM history GROUP BY paid_status")
                rows = cursor.fetchall()
                data = {row[0]: row[1] for row in rows}
                for k in ["Paid", "Unpaid", "Pending"]:
                    if k not in data: data[k] = 0
                return data
        except: return {"Paid": 0, "Unpaid": 0, "Pending": 0}

    def get_daily_trend(self, days=7):
        """Return ([dates], [counts]) for the last N days"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days-1)
            
            date_map = defaultdict(int)
            for i in range(days):
                d = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
                date_map[d] = 0
                
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT substr(timestamp, 1, 10) as day, COUNT(*) 
                    FROM history 
                    WHERE day >= ? 
                    GROUP BY day
                """, (start_date.strftime("%Y-%m-%d"),))
                
                rows = cursor.fetchall()
                for r in rows:
                    if r[0] in date_map:
                        date_map[r[0]] = r[1]
            
            sorted_dates = sorted(date_map.keys())
            counts = [date_map[d] for d in sorted_dates]
            display_dates = [datetime.strptime(d, "%Y-%m-%d").strftime("%b %d") for d in sorted_dates]
            
            return display_dates, counts
            
        except Exception as e:
            print(f"Analytics Error: {e}")
            return [], []

    def get_recent_history(self, limit=5):
        """Fetch last N records"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM history ORDER BY timestamp DESC LIMIT ?", (limit,))
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except: return []
