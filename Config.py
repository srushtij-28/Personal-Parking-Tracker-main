from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "parking_records.json"

TOTAL_PARKING_SLOTS = 10
HOURLY_RATE = 20
