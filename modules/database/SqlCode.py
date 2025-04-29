import sqlite3
import sys
import os
import json

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

db_path = os.path.join(os.path.dirname(__file__), 'database.db')
db = Database(db_path)

sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
import functions

class dbmanager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def get_safes_by_owner(self, owner_id):
        self.cursor.execute("SELECT safe_id, safe_name FROM safe WHERE safe_owner = ?", (owner_id,))
        safes = self.cursor.fetchall()
        return safes

    def add_safe_balance(self, safebalance, safeid):
        self.cursor.execute("UPDATE `safe` SET `safe_balance` = `safe_balance` + ? WHERE safe_id = ?", (safebalance, safeid,))
        self.conn.commit()
        return

    def take_safe_balance(self, safebalance, safeid):
        self.cursor.execute("UPDATE `safe` SET `safe_balance` = `safe_balance` - ? WHERE safe_id = ?", (safebalance, safeid,))
        self.conn.commit()
        return

    def set_safe_name_db(self, safe_name, safeid):
        self.cursor.execute("UPDATE `safe` SET `safe_name` = ? WHERE safe_id = ?", (safe_name, safeid,))
        self.conn.commit()
        return

    def get_safe_information(self, safe_id):
        self.cursor.execute("SELECT * FROM safe WHERE safe_id = ? LIMIT 1", (safe_id,))
        rows = self.cursor.fetchall()

        if rows:
            safe_information = []
            for row in rows:
                created_date_str = functions.format_date(row[5], 2)
                difference_date_str = functions.days_since(created_date_str)
                safe = {
                    "safe_created": created_date_str,
                    "safe_difference": difference_date_str,
                    "safe_id": row[0],
                    "safe_name": row[1],
                    "safe_owner": row[2],
                    "safe_balance": row[3],
                    "safe_valute": row[4],
                    "safe_aimsum": row[6],
                    "safe_created_py": row[5],
                }
                safe_information.append(safe)
            return json.dumps(safe_information, ensure_ascii=False)

        return json.dumps([])

    def get_safe_name(self, safe_id):
        self.cursor.execute("SELECT safe_name FROM safe WHERE safe_id = ?", (safe_id,))
        safes = self.cursor.fetchall()
        if safes:
            return safes[0][0]
        else:
            return None

    def close(self):
        self.conn.close()