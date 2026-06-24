from pathlib import Path
import sqlite3
import random
import time
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# --- 1. REAL DATABASE INITIALIZATION (SQLite) ---
script_dir = Path(__file__).resolve().parent
DB_NAME = f"{script_dir}/digital_twin_telemetry.db"

def init_db():
    """Creates the telemetry table if it doesn't exist."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                temperature_c REAL,
                rpm INTEGER,
                status TEXT
            )
        """)
        conn.commit()

def save_telemetry_to_db(temp, rpm, status):
    """Inserts a real sensor reading into the SQL database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO telemetry (temperature_c, rpm, status) VALUES (?, ?, ?)",
            (temp, rpm, status)
        )
        conn.commit()

# --- 2. BI-DIRECTIONAL TOOLS FOR THE AGENT ---
def get_historical_telemetry():
    """DATABASE TOOL: Fetches the last 5 real database logs for trend analysis."""
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, temperature_c, rpm, status FROM telemetry ORDER BY id DESC LIMIT 5")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def execute_emergency_shutdown():
    """ACTUATOR TOOL: Sends a critical safety shutdown signal back to the machine."""
    print("\n[PHYSICAL SYSTEM SIGNAL] 🚨 SHUTTING DOWN ENGINE IMMINENTLY... 🚨")
    return "Success: Physical asset safely brought to a SHUTDOWN state."

# --- 3. DIGITAL TWIN AGENT ---
digital_twin_brain = Agent(
    model=OpenAIChat(
        id="lm-studio-local",
        base_url="http://192.168.1.111:1234/v1"
    ),
    tools=[get_historical_telemetry, execute_emergency_shutdown],
    instructions=[
        "You are an automated Digital Twin monitor running on a continuous loop.",
        "1. Call 'get_historical_telemetry' to pull the newest records from the SQLite database.",
        "2. Analyze the data stream. If the most recent temperature exceeds 100°C, it is an anomaly.",
        "3. If an anomaly is found, call 'execute_emergency_shutdown' immediately.",
        "4. Provide a very brief, 2-line summary of your audit. Be direct and technical."
    ],
    markdown=True
)

# --- 4. CONTINUOUS SIMULATION LOOP ---
def run_digital_twin_simulation():
    init_db()
    print("--- Digital Twin Live Monitoring Initialized (Press Ctrl+C to stop) ---")
    
    current_status = "RUNNING"
    
    while True:
        # Simulate real physical hardware generating raw data
        # Most of the time it's safe (75-90), occasionally it spikes to 115
        simulated_temp = random.choice([75, 82, 88, 91, 115]) if current_status == "RUNNING" else 0
        simulated_rpm = random.randint(2800, 3600) if current_status == "RUNNING" else 0
        
        # 1. Physical World: Save telemetry to the real SQL database
        save_telemetry_to_db(simulated_temp, simulated_rpm, current_status)
        print(f"\n[Sensors synced to DB] Temp: {simulated_temp}°C | RPM: {simulated_rpm} | Status: {current_status}")
        
        # 2. Digital World: Pass control to the Agno Agent to audit the database
        print("[Twin Brain] Auditing database logs...")
        response = digital_twin_brain.run("Audit database logs and react if hardware is failing.")
        
        # Output the agent's summary
        print(response.content)
        
        # Intercept if the agent decided a shutdown command was sent
        # (In a real system, the tool modifies the hardware state directly)
        if "SHUTDOWN" in response.content or simulated_temp > 100:
            current_status = "SHUTDOWN"
            print("\n[System Locked] Twin enforced shutdown. Terminating loop.")
            break
            
        # Wait 5 seconds before the next physical sensor sweep
        time.sleep(5)

if __name__ == "__main__":
    run_digital_twin_simulation()