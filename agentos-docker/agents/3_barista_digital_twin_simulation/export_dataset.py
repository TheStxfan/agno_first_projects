import json
import sqlite3
from pathlib import Path
from config import DB_URL

# Definiamo il percorso del file JSONL finale nella stessa cartella
script_dir = Path(__file__).resolve().parent
OUTPUT_JSONL = f"{script_dir}/barista_chat_dataset.jsonl"

def export_db_to_jsonl():
    # Puliamo l'URL di Agno (sqlite:///) per renderlo compatibile con sqlite3 nativo
    db_path = DB_URL.replace("sqlite:///", "")
    print(f"Connessione al database: {db_path}")
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Permette di accedere alle colonne per nome (es. row["role"])
    cursor = conn.cursor()
    
    try:
        # 1. Troviamo tutti i session_id univoci presenti nella tabella dei messaggi
        cursor.execute("SELECT session_id FROM sessions WHERE exported_to_jsonl = 0")
        sessions = cursor.fetchall()
        
        if not sessions:
            print("Nessun messaggio trovato nel database. Esegui prima qualche simulazione!")
            return
            
        print(f"Trovate {len(sessions)} NUOVE sessioni di chat. Inizio formattazione e append...")
        
        contatore = 0
           
        # 2. Apriamo il file JSONL
        with open(OUTPUT_JSONL, "a", encoding="utf-8") as jsonl_file:
            for session in sessions:
                s_id = session["session_id"]
                
                # Prendiamo tutti i messaggi della sessione corrente ordinati cronologicamente
                cursor.execute(
                    "SELECT role, content FROM chat_messages WHERE session_id = ? ORDER BY timestamp ASC",
                    (s_id,)
                )
                messages_rows = cursor.fetchall()
                
                # Se per qualche motivo la sessione è vuota, saltiamo l'esportazione per evitare righe vuote
                if not messages_rows:
                    continue

                # Creiamo la lista di dizionari con il formato di chat standard
                conversation_messages = []
                for row in messages_rows:
                    conversation_messages.append({
                        "role": row["role"],
                        "content": row["content"]
                    })
                
                # Struttura finale della riga (formato Conversational per LLM)
                jsonl_row = {
                    "messages": conversation_messages
                }
                
                # Serializzazione in stringa JSON
                json_string = json.dumps(jsonl_row, ensure_ascii=False)
                
                # Scriviamo la riga nel file aggiungendo un UNICO \n alla fine
                jsonl_file.write(json_string + "\n")
                
                # AGGIUNTO: Aggiorniamo il database marcando la sessione corrente come esportata
                cursor.execute(
                    "UPDATE sessions SET exported_to_jsonl = 1 WHERE session_id = ?",
                    (s_id,)
                )
                contatore += 1    

        print(f"Esportazione completata! {contatore} conversazioni esportate.")
        print(f"File pronto in: {OUTPUT_JSONL}")
        
    except sqlite3.OperationalError as e:
        print(f"Errore durante l'accesso al database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    export_db_to_jsonl()