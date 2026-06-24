from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb 
from config import DB_URL

def make_barista_agent(session_id: str) -> Agent:
    return Agent(
        model=OpenAIChat(
            id="lm-studio-local",
            base_url="http://192.168.1.111:1234/v1",
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
        ],
        markdown=False,
    )
