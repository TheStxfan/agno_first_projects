from pathlib import Path
from dotenv import load_dotenv
from service.simulation_service import run_continuous
from dao.session_dao import get_all_sessions, init_custom_db
from export_dataset import export_db_to_jsonl

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


def main():
    init_custom_db()
    # Modifica num_sessions per quante conversazioni vuoi generare
    run_continuous(num_sessions=5)
    # print(get_all_sessions())
    export_db_to_jsonl()


if __name__ == "__main__":
    main()