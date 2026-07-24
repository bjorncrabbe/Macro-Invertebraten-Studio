"""
session.py

Beheer van een staal (sessie).
"""

from __future__ import annotations

import json
import os
from datetime import datetime

from config import DATA_FOLDER


class SessionManager:

    def __init__(self):

        self.location = None
        self.operator = None
        self.folder = None
        self.observations = 0

    def create(self, location: str, operator: str):

        self.location = location
        self.operator = operator

        self.folder = os.path.join(
            DATA_FOLDER,
            location
        )

        os.makedirs(self.folder, exist_ok=True)

        os.makedirs(
            os.path.join(self.folder, "screenshots"),
            exist_ok=True
        )

        self.save()

    def save(self):

        if self.folder is None:
            return

        data = {

            "location": self.location,

            "operator": self.operator,

            "created": datetime.now().isoformat(),

            "observations": self.observations

        }

        with open(

            os.path.join(self.folder, "session.json"),

            "w",

            encoding="utf8"

        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    def load(self, location):

        folder = os.path.join(
            DATA_FOLDER,
            location
        )

        file = os.path.join(
            folder,
            "session.json"
        )

        if not os.path.exists(file):
            return False

        with open(file, encoding="utf8") as f:

            data = json.load(f)

        self.location = data["location"]
        self.operator = data["operator"]
        self.folder = folder
        self.observations = data.get(
            "observations",
            0
        )

        return True

    def add_observation(self):

        self.observations += 1

        self.save()