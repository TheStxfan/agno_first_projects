from pathlib import Path
from dotenv import load_dotenv

from dao.telemetry_dao import init_db
from service.twin_service import run_simulation

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


def main():
    init_db()
    print("--- Digital Twin Live Monitoring Initialized (Press Ctrl+C to stop) ---")
    run_simulation()


if __name__ == "__main__":
    main()