import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG_FILE = ROOT / "config.yaml"

if not CONFIG_FILE.exists():
    raise FileNotFoundError(f"Configuration file not found: {CONFIG_FILE}")

with CONFIG_FILE.open("r", encoding="utf-8") as f:
    config = yaml.safe_load(f) or {}


def abs_path(path_str: str) -> Path:
    path = Path(path_str)
    return path if path.is_absolute() else (ROOT / path)
