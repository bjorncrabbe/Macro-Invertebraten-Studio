import os
from config import KEY_PATH

print(KEY_PATH)
print(os.path.exists(KEY_PATH))
from backend.determination import DeterminationEngine

key = DeterminationEngine()

print(key.get_options())