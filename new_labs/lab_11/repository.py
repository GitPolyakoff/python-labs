import sqlite3
from models import Account

class AccountRepository:
    def __init__(self, db_path="bank.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        #подключаюсь к файлу SQLite
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            with open('schema.sql', 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
            # пустая ли база, чтобы заполнить
            cursor = conn.execute("SELECT COUNT(*) FROM clients")
            if cursor.fetchone()[0] == 0:
                with open('seed.sql', 'r', encoding='utf-8') as f:
                    conn.executescript(f.read())

    def get_all(self):
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT a.id, c.name as client_name, a.balance, a.status 
                FROM accounts a
                JOIN clients c ON a.client_id = c.id
            """).fetchall()
            return [dict(row) for row in rows]

    def get_by_id(self, acc_id: int):
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM accounts WHERE id = ?", (acc_id,)).fetchone()
            return dict(row) if row else None

    def create(self, client_id: int, balance: float, status: str):
        with self._get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO accounts (client_id, balance, status) VALUES (?, ?, ?)",
                (client_id, balance, status)
            )
            return cursor.lastrowid

    #транзакция перевод денег
    def transfer_money(self, from_id: int, to_id: int, amount: float):
        conn = self._get_connection()
        try:
            with conn:
                # проверка баланса
                sender = conn.execute("SELECT balance FROM accounts WHERE id = ?", (from_id,)).fetchone()
                if not sender or sender['balance'] < amount:
                    raise ValueError("Недостаточно средств или счет не найден")
                # списание
                conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_id))
                # начисление
                conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_id))
        except Exception as e:
            raise e
        finally:
            conn.close()