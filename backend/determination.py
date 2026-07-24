import csv
import os

from config import DETERMINATION_PATH

class DeterminationEngine:

    def __init__(self):

        self.database = {}

        self.current_step = "stap_1"

        self.result = None

        print(self.database)

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
                encoding="utf-8-sig"
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

        if keuze["result"] is not None:

            self.result = keuze["result"]

            return True

        self.current_step = keuze["next"]

        return False

    def reset(self):
        """Reset de determinatiesleutel."""

        self.current_step = "stap_1"
        self.result = None

    def get_result(self):
        """Geef het huidige resultaat terug."""

        return self.result

    def is_finished(self):
        """Controleer of de determinatie voltooid is."""

        return self.result is not None
if __name__ == "__main__":

    engine = DeterminationEngine()

    while not engine.is_finished():

        print(f"\n--- {engine.current_step} ---")

        opties = engine.get_options()

        for optie, gegevens in opties.items():
            print(f"{optie}: {gegevens['tekst']}")

        keuze = input("Maak een keuze (A/B): ").upper()

        if keuze not in opties:
            print("Ongeldige keuze.")
            continue

        engine.answer(keuze)

    print("\nResultaat:")
    print(engine.get_result())