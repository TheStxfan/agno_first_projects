import random
import time

from dao.telemetry_dao import save_telemetry
from agent.twin_agent import digital_twin_brain

TEMP_POOL = [75, 82, 88, 91, 115]
SHUTDOWN_KEYWORD = "SHUTDOWN"
ANOMALY_THRESHOLD = 100


def _simulate_sensors(status: str) -> tuple[float, int]:
    if status != "RUNNING":
        return 0.0, 0
    temp = random.choice(TEMP_POOL)
    rpm = random.randint(2800, 3600)
    return temp, rpm


def _is_shutdown_triggered(agent_response: str, temp: float) -> bool:
    return SHUTDOWN_KEYWORD in agent_response or temp > ANOMALY_THRESHOLD


def run_simulation():
    status = "RUNNING"

    while True:
        temp, rpm = _simulate_sensors(status)
        save_telemetry(temp, rpm, status)
        print(f"\n[Sensors synced to DB] Temp: {temp}°C | RPM: {rpm} | Status: {status}")

        print("[Twin Brain] Auditing database logs...")
        response = digital_twin_brain.run("Audit database logs and react if hardware is failing.")
        print(response.content)

        if _is_shutdown_triggered(response.content, temp):
            status = "SHUTDOWN"
            print("\n[System Locked] Twin enforced shutdown. Terminating loop.")
            break

        time.sleep(5)