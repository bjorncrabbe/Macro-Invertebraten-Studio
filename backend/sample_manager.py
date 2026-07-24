"""
sample_manager.py

Beheer van het huidige staal.
"""

from __future__ import annotations

import json
import os
from datetime import datetime

from config import DATA_FOLDER


class SampleManager:

    def __init__(self):

        self.meetpunt = None
        self.locatie = None
        self.operator_id = None

        self.sample_folder = None
        self.csv_file = None
        self.session_file = None
        self.screenshots_folder = None

        self.observation_count = 0

        self.started = None
        self.status = "closed"

    # --------------------------------------------------
    # Nieuw staal
    # --------------------------------------------------

    def create_sample(
        self,
        meetpunt,
        operator_id
    ):

        self.meetpunt = str(meetpunt)

        self.operator_id = operator_id

        self.sample_folder = os.path.join(
            DATA_FOLDER,
            self.meetpunt
        )

        self.csv_file = os.path.join(
            self.sample_folder,
            "observations.csv"
        )

        self.session_file = os.path.join(
            self.sample_folder,
            "session.json"
        )

        self.screenshots_folder = os.path.join(
            self.sample_folder,
            "screenshots"
        )

        os.makedirs(
            self.screenshots_folder,
            exist_ok=True
        )

        self.started = datetime.now()

        self.observation_count = 0

        self.status = "open"

        self.save_session()

    # --------------------------------------------------
    # Bestaand staal openen
    # --------------------------------------------------

    def open_sample(self, meetpunt):

        self.meetpunt = str(meetpunt)

        self.sample_folder = os.path.join(
            DATA_FOLDER,
            self.meetpunt
        )

        self.csv_file = os.path.join(
            self.sample_folder,
            "observations.csv"
        )

        self.session_file = os.path.join(
            self.sample_folder,
            "session.json"
        )

        self.screenshots_folder = os.path.join(
            self.sample_folder,
            "screenshots"
        )

        if not os.path.exists(self.session_file):
            return False

        with open(
            self.session_file,
            "r",
            encoding="utf8"
        ) as file:

            data = json.load(file)

        self.meetpunt = data["meetpunt"]
        self.locatie = data["locatie"]

        self.operator_id = data["operator_id"]

        self.observation_count = data["observation_count"]

        self.status = data["status"]

        if data["started"]:

            self.started = datetime.fromisoformat(
                data["started"]
            )

        return True

    # --------------------------------------------------
    # Opslaan
    # --------------------------------------------------

    def save_session(self):

        data = {

            "meetpunt": self.meetpunt,

            "operator_id": self.operator_id,

            "started": (
                self.started.isoformat()
                if self.started else None
            ),

            "observation_count": self.observation_count,

            "status": self.status

        }

        with open(
            self.session_file,
            "w",
            encoding="utf8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    # --------------------------------------------------
    # Teller
    # --------------------------------------------------

    def increment_counter(self):

        self.observation_count += 1

        self.save_session()

    # --------------------------------------------------
    # Afsluiten
    # --------------------------------------------------

    def close_sample(self):

        self.status = "closed"

        self.save_session()