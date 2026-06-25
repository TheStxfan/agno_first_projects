from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb 
from config import DB_URL


def make_customer_agent(tone: str, session_id: str) -> Agent:
    """
    Crea un agente customer con il tono specificato.
    La storia della sessione viene persistita automaticamente su PostgreSQL.
    """
    return Agent(
        model=OpenAIChat(
        id="meta/llama-3.3-70b-instruct",
        base_url="https://integrate.api.nvidia.com/v1"
        ),
        session_id=session_id,
        db=SqliteDb(
            session_table="customer_sessions",
            db_url=DB_URL,
        ),
        instructions=[
            f"Sei un cliente di un bar. Il tuo tono è: {tone}.",
            "Fai richieste tipiche da bar: caffè, cappuccino, cornetto, succhi, ecc.",
            "Rimani sempre nel personaggio. Non spiegare il tuo tono, mostralo.",
            "Ogni messaggio deve essere una singola frase breve, come in una vera conversazione al banco.",
        ],
        markdown=False,
    )