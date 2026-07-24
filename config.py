"""
Macro-Invertebraten Studio v4.0
Configuratiebestand
"""

import os

# Hoofdmap van het project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Camera
CAMERA_INDEX = 0
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
CAMERA_FPS = 30

# AI
MODEL_PATH = os.path.join(BASE_DIR, "keras_model.h5")
LABELS_PATH = os.path.join(BASE_DIR, "labels.txt")

# Determinatiesleutel
KEY_PATH = os.path.join(
    BASE_DIR,
    "data",
    "key.csv"
)
DETERMINATION_PATH = os.path.join(
    BASE_DIR,
    "data",
    "determination"
)
# Mappen
SCREENSHOT_FOLDER = os.path.join(BASE_DIR, "screenshots")
LOG_FOLDER = os.path.join(BASE_DIR, "logs")
DATA_FOLDER = os.path.join(BASE_DIR, "data")

# CSV
CSV_FILE = os.path.join(DATA_FOLDER, "waarnemingen.csv")

# AI
AI_INPUT_SIZE = 224
AI_SCAN_INTERVAL = 10
AI_MIN_CONFIDENCE = 0.60
DATA_FOLDER = os.path.join(BASE_DIR, "data")

OPERATORS_FILE = os.path.join(
    DATA_FOLDER,
    "operators.json"
)