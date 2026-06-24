from dao.telemetry_dao import get_last_n


def get_historical_telemetry() -> list[dict]:
    """DATABASE TOOL: Fetch the last 5 telemetry records for trend analysis."""
    return get_last_n(5)


def execute_emergency_shutdown() -> str:
    """ACTUATOR TOOL: Send a critical safety shutdown signal to the machine."""
    print("\n[PHYSICAL SYSTEM SIGNAL] 🚨 SHUTTING DOWN ENGINE IMMINENTLY... 🚨")
    return "Success: Physical asset safely brought to a SHUTDOWN state."