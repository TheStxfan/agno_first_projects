from agno.agent import Agent
from agno.models.openai import OpenAIChat
from tools.agent_tools import get_historical_telemetry, execute_emergency_shutdown

digital_twin_brain = Agent(
    model=OpenAIChat(
        id="lm-studio-local",
        base_url="http://192.168.1.111:1234/v1",
    ),
    tools=[get_historical_telemetry, execute_emergency_shutdown],
    instructions=[
        "You are an automated Digital Twin monitor running on a continuous loop.",
        "1. Call 'get_historical_telemetry' to pull the newest records from the SQLite database.",
        "2. Analyze the data stream. If the most recent temperature exceeds 100°C, it is an anomaly.",
        "3. If an anomaly is found, call 'execute_emergency_shutdown' immediately.",
        "4. Provide a very brief, 2-line summary of your audit. Be direct and technical.",
    ],
    markdown=True,
)