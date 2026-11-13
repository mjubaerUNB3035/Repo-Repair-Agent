# config.py
# Central settings 

import os
from dataclasses import dataclass, field
from pathlib import Path


# Project root 
def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


@dataclass
class Settings:
    # Model
    ollama_url: str = "http://localhost:11434"
    model_name: str = "qwen2.5-coder:14b"

    # Agent Limit
    max_steps: int = 30
    max_seconds: int = 900
    max_retries: int = 2

    # Pilot gate
    pilot_size: int = 20
    pilot_min_resolved: int = 4

    # Output folders.
    data_dir: Path = field(default_factory=lambda: project_root() / "data")
    runs_dir: Path = field(default_factory=lambda: project_root() / "runs")


# Load settings
def load_settings() -> Settings:
    settings = Settings()
    if os.getenv("OLLAMA_URL"):
        settings.ollama_url = os.environ["OLLAMA_URL"]
    if os.getenv("REPAIR_MODEL"):
        settings.model_name = os.environ["REPAIR_MODEL"]
    return settings
