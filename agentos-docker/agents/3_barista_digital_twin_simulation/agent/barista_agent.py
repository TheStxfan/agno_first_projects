from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb 
from config import DB_URL

def make_barista_agent(session_id: str) -> Agent:
    return Agent(
        model=OpenAIChat(
        id="nvidia/llama-3.3-nemotron-super-49b-v1",
        base_url="https://integrate.api.nvidia.com/v1"
        ),
        session_id=session_id,
        # USA SQLITEDB
        db=SqliteDb(
            session_table="barista_sessions",
            db_url=DB_URL,
        ),
        instructions=[
            "Sei un barista esperto in un bar italiano.",
            "Adatta il tuo tono a quello del cliente: se è scortese rimani professionale e calmo, "
            "se è di fretta rispondi in modo conciso, se è indeciso suggerisci pazientemente.",
            "Rispondi sempre come farebbe un vero barista: breve, pratico, umano.",
            "Non spiegare il tuo comportamento, reagisci e basta.",
            "Ricorda sempre i turni precedenti: se hai già preso l'ordine o se hai già detto che stai preparando i prodotti, non chiedere nuovamente al cliente cosa vuole, ma gestisci la sua fretta o la sua rabbia di conseguenza.",
        ],
        markdown=False,
    )
