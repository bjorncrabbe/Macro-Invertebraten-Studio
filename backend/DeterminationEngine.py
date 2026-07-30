"""
Determination Engine

Leest determinatiesleutels uit CSV-bestanden
en doorloopt de sleutel stap voor stap.
"""

import csv
import os

from config import DETERMINATION_PATH


class DeterminationEngine:

    LOAD_PREFIX = "LOAD:"

    def __init__(self):

        self.database = {}
        self.current_step = "stap_1"
        self.result = None

    def load(self, key_name):

        path = os.path.join(
            DETERMINATION_PATH,
            f"{key_name}.csv"
        )

        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Sleutelbestand niet gevonden: {path}"
            )

        self.database.clear()
        self.current_step = "stap_1"
        self.result = None

        with open(
                path,
                newline="",
                encoding="utf8-sig"
        ) as file:

            reader = csv.DictReader(file, delimiter=";")

            for row in reader:

                step = row["ID"]
                option = row["OPTIE"]

                if step not in self.database:
                    self.database[step] = {}

                self.database[step][option] = {

                    "tekst": row["TEKST"],

                    "next": (
                        None
                        if row["VOLGENDE"] == ""
                        else row["VOLGENDE"]
                    ),

                    "result": (
                        None
                        if row["RESULTAAT"] == ""
                        else row["RESULTAAT"]
                    )
                }

    def get_options(self):

        if self.current_step not in self.database:
            return None

        return self.database[self.current_step]

    def answer(self, option):

        options = self.get_options()

        if options is None:
            return False

        if option not in options:
            return False

        keuze = options[option]

        # Resultaat bereikt
        if keuze["result"] is not None:

            # Andere determinatiesleutel laden
            if keuze["result"].startswith(self.LOAD_PREFIX):

                key_name = keuze["result"][len(self.LOAD_PREFIX):]

                self.load(key_name)

                return False

            # Eindresultaat (familie)
            self.result = keuze["result"]

            return True

        # Naar volgende stap
        self.current_step = keuze["next"]

        return False

    def reset(self):

        self.current_step = "stap_1"
        self.result = None

    def get_result(self):

        return self.result

    def is_finished(self):

        return self.result is not None