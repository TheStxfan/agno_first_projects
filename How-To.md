### Pgvector Database Structure Incompatibility (PostgreSQL 18+ Upgrade)

- **Technologies:** Docker, PostgreSQL, Pgvector
- **Context:** Upgrading the `pgvector` container image to a version based on PostgreSQL 18+ while retaining a volume or directory containing data initialized by an older PostgreSQL version.
- **Problem/Log:**

```text
pgvector  | Error: in 18+, these Docker images are configured to store database data in a
pgvector  |        format which is compatible with "pg_ctlcluster" (specifically, using
pgvector  |        major-version-specific directory names).  This better reflects how
pgvector  |        PostgreSQL itself works, and how upgrades are to be performed.
pgvector  |
pgvector  |        See also https://github.com/docker-library/postgres/pull/1259
pgvector  |
pgvector  |        Counter to that, there appears to be PostgreSQL data in:
pgvector  |          /var/lib/postgresql/data (unused mount/volume)
pgvector  |
pgvector  |        This is usually the result of upgrading the Docker image without
pgvector  |        upgrading the underlying database using "pg_upgrade" (which requires both
pgvector  |        versions).

```

- **Solution:**
  Clear the old, incompatible database volume and restart the container setup to let PostgreSQL 18+ initialize its new internal directory structure from scratch.

```bash
docker compose down -v
docker compose up -d

```

---

### Application Connection Refused (Database Host Misconfiguration)

- **Technologies:** Docker, Python, Agno, Psycopg
- **Context:** The `agentos-api` container application trying to establish a connection to the PostgreSQL/Pgvector database container.
- **Problem/Log:**

```text
agentos-api  | ERROR    Error checking if table exists: (psycopg.OperationalError) connection
agentos-api  |          failed: connection to server at "127.0.0.1", port 5432 failed:
agentos-api  |          Connection refused
agentos-api  |                  Is the server running on that host and accepting TCP/IP
agentos-api  |          connections?
agentos-api  |          Multiple connection attempts failed. All failures were:
agentos-api  |          - host: 'localhost', port: 5432, hostaddr: '::1': connection failed:
agentos-api  |          connection to server at "::1", port 5432 failed: Connection refused

```

- **Solution:**
  Change the default fallback value of the database host from `localhost` to the explicit Docker Compose service name (`pgvector`) in the database URL configuration module `db/url.py`.

```python
host = getenv("DB_HOST", "pgvector")

```

---

### Duplicate Database ID Warning in Agno Registry

- **Technologies:** Python, Agno, PostgreSQL
- **Context:** Instantiating multiple agent or database session storage components across the application, which concurrently call the database initializer function.
- **Problem/Log:**

```text
agentos-api  | WARNING  Registry: multiple distinct databases share id 'agentos-db'; keeping
agentos-api  |          the first. Give them distinct ids to avoid one shadowing the other.

```

- **Solution:**
  Update `session.py` to include a global call counter that dynamically appends a unique sequential suffix to `DB_ID` every time `get_postgres_db()` is invoked. This ensures distinct IDs in the global registry without changing individual agent invocation files.

```python
from agno.db.postgres import PostgresDb
from agno.knowledge import Knowledge
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.vectordb.pgvector import PgVector, SearchType

from db.url import db_url

DB_ID = "agentos-db"
_db_call_count = 0

def get_postgres_db(contents_table: str | None = None) -> PostgresDb:
    """Create a PostgresDb instance with a unique sequential ID."""
    global _db_call_count
    _db_call_count += 1
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

```
