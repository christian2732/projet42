# Objectif : Charger la configuration depuis config.yaml

import yaml
from pathlib import Path

class Settings:
    def __init__(self):
        config_path = Path(__file__).resolve().parent.parent.parent / "config" / "config.yaml"
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        self.app = config.get("app", {})

settings = Settings()
