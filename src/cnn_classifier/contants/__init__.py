from pathlib import Path

# Get the project root directory (two levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

CONFIG_FILE_PATH: Path = PROJECT_ROOT / "config" / "config.yaml"
PARAMS_FILE_PATH: Path = PROJECT_ROOT / "params.yaml"