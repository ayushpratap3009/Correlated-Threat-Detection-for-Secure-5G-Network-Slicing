import json
import os
from datetime import datetime

ALERT_FILE = "alerts_log.json"


def _safe_load():
    """Load alerts safely even if file is empty/corrupted."""
    if not os.path.exists(ALERT_FILE):
        return []

    try:
        with open(ALERT_FILE, "r") as f:
            return json.load(f)
    except:
        # file empty or corrupted → reset
        return []


def save_alert(alert):
    """
    Save alert safely to alerts_log.json
    """

    alert["slice"] = str(alert["slice"])
    alert["attack"] = str(alert["attack"])
    alert["confidence"] = float(alert["confidence"])
    alert["severity"] = str(alert["severity"])
    alert["time"] = datetime.utcnow().strftime("%H:%M:%S")

    data = _safe_load()

    data.append(alert)

    with open(ALERT_FILE, "w") as f:
        json.dump(data, f, indent=2)