import os
from pathlib import Path
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.file import FileTools

env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

CARTELLA_DOCUMENTI = "/mnt/Files/TTF/! Tirocinio/Anno I/Coding/agno/agentos-docker/"

api_key_locale = os.getenv("OPENAI_API_KEY") 

agent = Agent(
    model=OpenAIChat(
        id="lm-studio-local",
        base_url="http://192.168.1.111:1234/v1"
    ),
    
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