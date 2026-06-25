import sqlite3
from config import DB_URL

def init_custom_db():
    db_path = DB_URL.replace("sqlite:///", "")
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # 1. Tabella delle Sessioni (Aggiunta colonna exported_to_jsonl)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            exported_to_jsonl INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        # 2. Tabella dei Messaggi
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT CHECK(role IN ('user', 'assistant', 'system')),
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        );
        """)
        conn.commit()

def insert_chat_message(session_id: str, role: str, content: str):
    db_path = DB_URL.replace("sqlite:///", "")
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Inserisce la sessione se non esiste già (grazie all'INSERT OR IGNORE)
        cursor.execute(
            "INSERT OR IGNORE INTO sessions (session_id) VALUES (?)", 
            (session_id,)
        )
        
        # Inserisce il singolo messaggio della chat
        cursor.execute(
            "INSERT INTO chat_messages (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, role, content)
        )
        conn.commit()

def get_all_sessions(table: str = "barista_sessions") -> list[dict]:
    """Recupera tutte le sessioni dalla tabella specificata."""
    db_path = DB_URL.replace("sqlite:///", "")
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT session_id, created_at FROM {table} ORDER BY created_at DESC")
        rows = cursor.fetchall()
        
    return [{"session_id": r[0], "created_at": r[1]} for r in rows]


def get_session_by_id(session_id: str, table: str = "barista_sessions") -> dict | None:
    """Recupera una sessione specifica per ID da SQLite."""
    db_path = DB_URL.replace("sqlite:///", "")
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT session_id, session_data FROM {table} WHERE session_id = ?",
            (session_id,),
        )
        row = cursor.fetchone()
        
    if row is None:
        return None
    return {"session_id": row[0], "memory": row[1]}


def get_chat_messages_by_session(session_id: str) -> list[dict]:
    """Recupera tutti i messaggi di chat per una sessione specifica."""
    db_path = DB_URL.replace("sqlite:///", "")
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role, content, timestamp FROM chat_messages WHERE session_id = ? ORDER BY timestamp ASC",
            (session_id,),
        )
        rows = cursor.fetchall()
        
    return [{"role": r[0], "content": r[1], "timestamp": r[2]} for r in rows]