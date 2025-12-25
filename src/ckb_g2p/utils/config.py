import yaml
from pathlib import Path
from functools import lru_cache

# Define the path to the configuration file relative to this script
# Structure: project_root/src/ckb_g2p/utils/config.py
# We need to go up 3 levels to find project_root/data/phonology.yaml
BASE_DIR = Path(__file__).resolve().parents[3]
CONFIG_PATH = BASE_DIR / "data" / "phonology.yaml"

@lru_cache(maxsize=1)
def load_config() -> dict:
    """
    Loads the YAML configuration file.
    Uses caching to ensure we only read from disk once.
    """
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"❌ Critical Error: Configuration file not found at: {CONFIG_PATH}\n"
            "Please ensure the 'data/phonology.yaml' file exists in your project root."
        )

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"❌ Error parsing YAML config: {e}")

def get_mappings() -> dict:
    """Helper to get just the Grapheme->IPA mapping."""
    return load_config().get("mappings", {})

def get_phoneme_features() -> dict:
    """Helper to get phoneme details (sonority, type)."""
    return load_config().get("phonemes", {})