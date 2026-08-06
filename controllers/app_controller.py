"""
Macro-Invertebraten Studio v4.0
App Controller

Verbindt de GUI met de backend.
"""

from __future__ import annotations

from backend.camera import Camera
from backend.ai_engine import AIEngine
from backend.determination import DeterminationEngine
from backend.count_manager import CountManager
from backend.sample_manager import SampleManager
from backend.operators import OperatorManager


class AppController:

    def __init__(self):

        # -------------------------------
        # Backend modules
        # -------------------------------

        self.camera = Camera()
        self.ai = AIEngine()

        # Determinatiesleutel
        self.key = DeterminationEngine()

        self.counter = CountManager()
        self.sample = SampleManager()
        self.operators = OperatorManager()

    # ==================================================
    # Camera
    # ==================================================

    def start_camera(self) -> bool:
        return self.camera.connect()

    def stop_camera(self) -> None:
        self.camera.disconnect()

    def get_frame(self):
        return self.camera.read()

    # ==================================================
    # AI
    # ==================================================

    def predict(self, frame):

        if frame is None:
            return None, 0.0

        return self.ai.predict_stable(frame)

    # ==================================================
    # Determinatiesleutel
    # ==================================================

    def load_key(self, key_name):

        print(f"AppController.load_key({key_name})")

        self.key.load(key_name)
        return True

    def get_options(self):
        return self.key.get_options()

    def choose(self, option: str):

        finished = self.key.answer(option)

        if finished:
            return True, self.key.get_result()

        return False, None

    def reset_key(self):
        self.key.reset()

    def get_result(self):
        return self.key.get_result()

    def is_finished(self):
        return self.key.is_finished()

    # ==================================================
    # Sample
    # ==================================================

    def new_sample(self, meetpunt, operator_id):

        self.sample.create_sample(
            meetpunt,
            operator_id
        )

    def open_sample(self, meetpunt):

        return self.sample.open_sample(
            meetpunt
        )

    def get_current_sample(self):

        return self.sample

    # ==================================================
    # Teller
    # ==================================================

    def add_count(self, family, genus):

        self.counter.add(
            family,
            genus
        )

    def remove_count(self, family, genus):

        self.counter.remove(
            family,
            genus
        )

    def get_counts(self):

        return self.counter.get_all()

    def get_total_count(self):

        return self.counter.get_total()

    def get_available_keys(self):
        return self.key.available_keys()

    def get_ai_labels(self):
        return self.ai.get_labels()