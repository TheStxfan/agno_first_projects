import os
from pathlib import Path
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat

# Trova il file .env partendo dalla posizione di questo script
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

agent = Agent(
    model=OpenAIChat(
        id="nvidia/nemotron-3-nano-30b-a3b",
        base_url="https://integrate.api.nvidia.com/v1"
    ),
    markdown=True,
    description="Sei un assistente AI che gira sugli endpoint di NVIDIA.",
)

agent.print_response("Spiegami brevemente cos'è una GPU")