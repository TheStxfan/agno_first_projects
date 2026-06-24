from pathlib import Path

# Configurazione generale della simulazione barista

# Definiamo il percorso del file del database SQLite
script_dir = Path(__file__).resolve().parent
DB_URL = f"sqlite:///{script_dir}/barista_sim.db"

# Toni disponibili per il customer agent
CUSTOMER_TONES = [
    "scortese e impaziente",
    "gentile e cordiale",
    "indeciso e confuso",
    "di fretta, parla velocemente",
    "sospettoso, fa molte domande",
    "allegro ed esuberante",
]

# Numero di turni di conversazione per sessione
TURNS_PER_SESSION = 3