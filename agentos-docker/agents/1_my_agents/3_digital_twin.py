import os
from pathlib import Path
import random
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

api_key_locale = os.getenv("OPENAI_API_KEY") 

# 1. Define a tool representing the "Physical Asset" data stream
def get_engine_telemetry():
    """Simulates real-time sensor data from a physical engine."""
    return {
        "temperature_c": random.choice([75, 82, 115, 79]),  # 115 is an anomaly!
        "rpm": random.randint(2500, 4000),
        "vibration_level": round(random.uniform(0.1, 0.9), 2)
    }

# 2. Initialize the Digital Twin Agent
engine_digital_twin = Agent(
    model=OpenAIChat(
        id="lm-studio-local",
        base_url="http://192.168.1.111:1234/v1"
    ),
    tools=[get_engine_telemetry],
    instructions=[
        "You are the Digital Twin of Engine-X100.",
        "Your job is to read the telemetry data from your physical counterpart.",
        "Analyze if the engine is running normally or if it requires emergency maintenance (e.g., temp > 100°C).",
        "Keep your assessment brief and highly technical."
    ],
    markdown=True
)

# 3. Run the Digital Twin simulation loop
print("--- Syncing Digital Twin with Physical Asset ---")
engine_digital_twin.print_response("Check current asset health and report anomalies.")