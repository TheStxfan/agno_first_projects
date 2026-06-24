import sqlite3

DB_NAME = "digital_twin_telemetry.db"


def init_db():
    """Crea la tabella telemetry se non esiste."""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                temperature_c REAL,
                rpm INTEGER,
                status TEXT
            )
        """)
        conn.commit()


def save_telemetry(temp: float, rpm: int, status: str):
    """Inserisce una riga di telemetria nel database."""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO telemetry (temperature_c, rpm, status) VALUES (?, ?, ?)",
            (temp, rpm, status),
        )
        conn.commit()


def get_last_n(n: int = 5) -> list[dict]:
    """Restituisce gli ultimi n record ordinati dal più recente."""
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT timestamp, temperature_c, rpm, status FROM telemetry ORDER BY id DESC LIMIT ?",
            (n,),
        ).fetchall()
    return [dict(row) for row in rows]