from agno.db.postgres import PostgresDb
from agno.knowledge import Knowledge
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.vectordb.pgvector import PgVector, SearchType

from db.url import db_url

DB_ID = "agentos-db"
# Contatore globale per rendere unici gli ID generati automaticamente
_db_call_count = 0

def get_postgres_db(contents_table: str | None = None) -> PostgresDb:
    """Create a PostgresDb instance with a unique sequential ID."""
    global _db_call_count
    _db_call_count += 1
    # Genera un ID unico come "agentos-db-1", "agentos-db-2", ecc.
    unique_id = f"{DB_ID}-{_db_call_count}"

    if contents_table is not None:
        return PostgresDb(id=unique_id, db_url=db_url, knowledge_table=contents_table)
    return PostgresDb(id=unique_id, db_url=db_url)


def create_knowledge(name: str, table_name: str) -> Knowledge:
    """Create a Knowledge instance with PgVector hybrid search."""
    return Knowledge(
        name=name,
        vector_db=PgVector(
            db_url=db_url,
            table_name=table_name,
            search_type=SearchType.hybrid,
            embedder=OpenAIEmbedder(id="text-embedding-3-small"),
        ),
        contents_db=get_postgres_db(contents_table=f"{table_name}_contents"),
    )