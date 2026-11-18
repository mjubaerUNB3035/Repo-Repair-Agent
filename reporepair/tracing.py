# tracing.py

import json
import time
from pathlib import Path

from reporepair.config import load_settings


# Start trace
def start_trace(instance_id: str) -> dict:
    trace = {
        "instance_id": instance_id,
        "started_at": time.time(),
        "events": [],
    }
    return trace


# Add event
def add_event(trace: dict, name: str, detail: str = "") -> None:
    event = {
        "name": name,
        "detail": detail,
        "at": time.time(),
    }
    trace["events"].append(event)


# Save trace
def save_trace(trace: dict) -> Path:
    settings = load_settings()
    settings.runs_dir.mkdir(parents=True, exist_ok=True)
    path = settings.runs_dir / (trace["instance_id"] + ".json")
    path.write_text(json.dumps(trace, indent=2), encoding="utf-8")
    return path
