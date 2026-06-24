import uuid
import random
from agent.customer_agent import make_customer_agent
from agent.barista_agent import make_barista_agent
from config import CUSTOMER_TONES, TURNS_PER_SESSION


def run_session(tone: str | None = None):
    """
    Esegue una singola sessione di conversazione barista/customer.
    Ogni sessione ha un UUID univoco — viene salvata automaticamente su PostgreSQL da Agno.
    """
    session_id = str(uuid.uuid4())
    tone = tone or random.choice(CUSTOMER_TONES)

    print(f"\n{'='*60}")
    print(f"[Sessione] {session_id}")
    print(f"[Tono cliente] {tone}")
    print(f"{'='*60}")

    customer = make_customer_agent(tone, session_id)
    barista = make_barista_agent(session_id)

    # Primo messaggio: il customer si avvicina al banco
    customer_msg = f"Entra nel bar con tono: {tone}. Fai la tua prima richiesta."

    for turn in range(TURNS_PER_SESSION):
        print(f"\n[Turno {turn + 1}]")

        # Customer parla
        customer_response = customer.run(customer_msg)
        customer_text = customer_response.content
        print(f"  Cliente : {customer_text}")

        # Barista risponde
        barista_response = barista.run(customer_text)
        barista_text = barista_response.content
        print(f"\n  Barista : {barista_text}")

        # Il customer reagisce alla risposta del barista nel turno successivo
        customer_msg = barista_text

    print(f"\n[Fine sessione — dati salvati su PostgreSQL]")
    return session_id


def run_continuous(num_sessions: int = 5):
    """Esegue più sessioni in sequenza con toni casuali."""
    print("--- Simulazione Barista/Customer avviata ---")
    for i in range(num_sessions):
        print(f"\n[Sessione {i+1}/{num_sessions}]")
        run_session()