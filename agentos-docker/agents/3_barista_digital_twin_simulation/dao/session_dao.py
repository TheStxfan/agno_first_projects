import psycopg
from config import DB_URL


def get_all_sessions(table: str = "barista_sessions") -> list[dict]:
    """
    Recupera tutte le sessioni salvate da Agno nel DB PostgreSQL.
    Utile per ispezionare i dati raccolti o esportarli per fine-tuning.
    """
    with psycopg.connect(DB_URL) as conn:
        rows = conn.execute(
            f"SELECT session_id, memory, created_at, updated_at FROM {table} ORDER BY updated_at DESC"
        ).fetchall()
    return [
        {"session_id": r[0], "memory": r[1], "created_at": r[2], "updated_at": r[3]}
        for r in rows
    ]


def get_session_by_id(session_id: str, table: str = "barista_sessions") -> dict | None:
    """Recupera una sessione specifica per ID."""
    with psycopg.connect(DB_URL) as conn:
        row = conn.execute(
            f"SELECT session_id, memory FROM {table} WHERE session_id = %s",
            (session_id,),
        ).fetchone()
    if row is None:
        return None
    return {"session_id": row[0], "memory": row[1]}