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

### PyTorch Inductor Configuration Attribute Error

- **Technologies:** Docker, PyTorch, Unsloth, Transformers
- **Context:** Building and running a Docker container to finetune a Llama-3-8b model using Unsloth where a specific mismatch between the installed PyTorch version and `unsloth_zoo` occurred.
- **Problem/Log:**

```text
AttributeError: module 'torch._inductor.config' has no attribute 'triton'

```

- **Solution:** Upgrade PyTorch to version `2.5.1` with explicit CUDA 12.4 support inside the `Dockerfile` to match the internal structure expected by the recent `unsloth_zoo` updates.

```dockerfile
RUN pip install --no-cache-dir torch==2.5.1 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

```

---

### TorchAO Integer Type Missing Attribute Error

- **Technologies:** Docker, PyTorch, TorchAO, Transformers, Unsloth
- **Context:** Launching the finetuning container after upgrading PyTorch, where bleeding-edge secondary dependencies introduced a conflict regarding low-bit quantization definitions.
- **Problem/Log:**

```text
  File "/usr/local/lib/python3.10/dist-packages/torchao/quantization/quant_primitives.py", line 191, in <module>
    torch.int1: (-(2**0), 2**0 - 1),
  File "/usr/local/lib/python3.10/dist-packages/torch/__init__.py", line 2562, in __getattr__
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
AttributeError: module 'torch' has no attribute 'int1'

```

- **Solution:** Pin the `transformers` library strictly to version `4.46.3` inside the `Dockerfile` to prevent it from pulling experimental `torchao` definitions that look for unreleased PyTorch features.

```dockerfile
RUN pip install --no-cache-dir transformers==4.46.3

```

---

### Unsloth Zoo Missing Package Metadata Error

- **Technologies:** Docker, Python, Unsloth
- **Context:** Importing `FastLanguageModel` from `unsloth` at the very beginning of the finetuning script inside the container execution phase.
- **Problem/Log:**

```text
  File "/usr/local/lib/python3.10/dist-packages/unsloth/_gpu_init.py", line 124, in <module>
    unsloth_zoo_version = importlib_version("unsloth_zoo")
  File "/usr/lib/python3.10/importlib/metadata/__init__.py", line 996, in version
    return distribution(distribution_name).version
  File "/usr/lib/python3.10/importlib/metadata/__init__.py", line 969, in distribution
    return Distribution.from_name(distribution_name)
  File "/usr/lib/python3.10/importlib/metadata/__init__.py", line 548, in from_name
    raise PackageNotFoundError(name)
importlib.metadata.PackageNotFoundError: No package metadata was found for unsloth_zoo

During handling of the above exception, another exception occurred:
...
ImportError: Unsloth: Please install unsloth_zoo via `pip install unsloth_zoo` then retry!

```

- **Solution:** Explicitly install `unsloth-zoo` directly from its GitHub repository via `pip` right before installing the main `unsloth` package inside the `Dockerfile`.

```dockerfile
RUN pip install --no-cache-dir "git+https://github.com/unslothai/unsloth-zoo.git" && \
    pip install --no-cache-dir "unsloth @ git+https://github.com/unslothai/unsloth.git"

```
