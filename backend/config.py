import os
from pathlib import Path

# Base directory of the silentbridge project
BASE_DIR = Path(__file__).resolve().parent

# --- HARDWARE & SYSTEM ---
CAMERA_INDEX = int(os.getenv("CAMERA_INDEX", 0))
FRAME_WIDTH = int(os.getenv("FRAME_WIDTH", 640))
FRAME_HEIGHT = int(os.getenv("FRAME_HEIGHT", 480))

# --- ML & MEDIAPIPE SETTINGS ---
MEDIAPIPE_CONFIDENCE = 0.7
PREDICTION_CONFIDENCE_THRESHOLD = 0.4

# --- LSTM CONFIGURATION ---
SEQUENCE_LENGTH = 80

# --- PATHS ---
# Using Path objects for absolute path resolution relative to this file
MODELS_DIR = BASE_DIR / "models"
MODEL_PATH_H5 = str(MODELS_DIR / "gesture_classifier.keras")

DATA_DIR = BASE_DIR / "data"
SEQUENCES_DIR = str(DATA_DIR / "sequences")
SIGN_DICT_PATH = str(DATA_DIR / "sign_dictionary.json")
SIGNS_DIR = str(DATA_DIR / "signs")

TRAINING_DIR = BASE_DIR / "training"
TRAINING_DATA_PATH = str(TRAINING_DIR / "gesture_data.csv")

# --- GUI & TTS ---
TTS_RATE = 150
TTS_VOLUME = 1.0
SIGN_DISPLAY_DELAY_MS = 2000   # pause between signs in queue
GUI_UPDATE_INTERVAL_MS = 30    # camera feed refresh rate

# Ensure essential directories exist when config is loaded
for directory in [MODELS_DIR, DATA_DIR, DATA_DIR / "sequences", DATA_DIR / "signs", TRAINING_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
