import uuid
import random
from agent.customer_agent import make_customer_agent
from agent.barista_agent import make_barista_agent
from config import CUSTOMER_TONES, TURNS_PER_SESSION
from dao.session_dao import insert_chat_message, init_custom_db # Importa le nuove funzioni

def run_session(tone: str | None = None):
    session_id = str(uuid.uuid4())
    tone = tone or random.choice(CUSTOMER_TONES)

    print(f"\n[Sessione] {session_id} - Tono: {tone}")

    customer = make_customer_agent(tone, session_id)
    barista = make_barista_agent(session_id)

    # Primo messaggio di attivazione
    customer_msg = f"Entra nel bar con tono: {tone}. Fai la tua prima richiesta."

    for turn in range(TURNS_PER_SESSION):
        print(f"\n[Turno {turn + 1}]")

        # 1. Il Customer (User) parla
        customer_response = customer.run(customer_msg)
        customer_text = customer_response.content
        print(f"  Cliente : {customer_text}")
        
        # SALVATAGGIO NEL DB DEL MESSAGGIO DEL CLIENTE
        insert_chat_message(session_id, role="user", content=customer_text)

        # 2. Il Barista (Assistant) risponde
        barista_response = barista.run(customer_text)
        barista_text = barista_response.content
        print(f"  Barista : {barista_text}")
        
        # SALVATAGGIO NEL DB DEL MESSAGGIO DEL BARISTA
        insert_chat_message(session_id, role="assistant", content=barista_text)

        # Il customer reagisce alla risposta del barista nel turno successivo
        customer_msg = barista_text

    return session_id

def run_continuous(num_sessions: int = 5):
    """Esegue più sessioni in sequenza con toni casuali."""
    print("--- Simulazione Barista/Customer avviata ---")
    for i in range(num_sessions):
        print(f"\n[Sessione {i+1}/{num_sessions}]")
        run_session()

