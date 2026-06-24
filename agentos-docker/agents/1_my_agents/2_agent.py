from pathlib import Path
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.file import FileTools

# Trova il file .env partendo dalla posizione di questo script
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

CARTELLA_DOCUMENTI = "/mnt/Files/TTF/! Tirocinio/Anno I/Coding/agno/agentos-docker/"

agent = Agent(
    model=OpenAIChat(
        id="nvidia/nemotron-3-nano-30b-a3b",
        base_url="https://integrate.api.nvidia.com/v1"
    ),
    # Diamo all'agente la capacità di leggere i file in quella cartella
    tools=[FileTools(base_dir=Path(CARTELLA_DOCUMENTI))],
    markdown=True,
    description="Sei un assistente AI capace di leggere file locali, capire cosa fanno e spiegarlo in poche parole e in modo chiaro.",
)

NOME_FILE = "compose.yaml"

agent.print_response(
    f"Per favore, leggi il file '{NOME_FILE}' che si trova nella tua cartella "
    f"e fammi un riassunto dettagliato dei punti chiave.",
    show_tools=True
)