from pathlib import Path
from dotenv import load_dotenv
from service.simulation_service import run_continuous

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


def main():
    # Modifica num_sessions per quante conversazioni vuoi generare
    run_continuous(num_sessions=5)


if __name__ == "__main__":
    main()