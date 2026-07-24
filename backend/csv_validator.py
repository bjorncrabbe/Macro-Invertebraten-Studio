"""
csv_validator.py

Controleert de structuur van een determinatie-CSV.
"""

import csv
import os


class CSVValidator:

    def __init__(self, filename):

        self.filename = filename

        self.rows = []

        self.ids = set()

        self.errors = []

        self.warnings = []

    # --------------------------------------------------
    # CSV laden
    # --------------------------------------------------

    def load(self):

        if not os.path.exists(self.filename):

            self.errors.append(
                "Bestand bestaat niet."
            )

            return False

        with open(
                self.filename,
                newline="",
                encoding="utf8"
        ) as file:

            reader = csv.DictReader(
                file,
                delimiter=";"
            )

            self.rows = list(reader)

        return True

    # --------------------------------------------------
    # Dubbele ID's
    # --------------------------------------------------

    def check_duplicate_ids(self):

        self.ids.clear()

        for row in self.rows:

            step = row["ID"]

            if step in self.ids:

                self.errors.append(
                    f"Dubbele ID gevonden: {step}"
                )

            self.ids.add(step)

    # --------------------------------------------------
    # Bestaat stap_1?
    # --------------------------------------------------

    def check_start(self):

        if "stap_1" not in self.ids:

            self.errors.append(
                "Startpunt 'stap_1' ontbreekt."
            )

    # --------------------------------------------------
    # Bestaat VOLGENDE?
    # --------------------------------------------------

    def check_next_steps(self):

        for row in self.rows:

            next_step = row["VOLGENDE"].strip()

            if next_step == "":
                continue

            if next_step not in self.ids:

                self.errors.append(
                    f"VOLGENDE bestaat niet: {next_step}"
                )

    # --------------------------------------------------
    # Eindstappen
    # --------------------------------------------------

    def check_results(self):

        for row in self.rows:

            volgende = row["VOLGENDE"].strip()

            resultaat = row["RESULTAAT"].strip()

            if volgende == "" and resultaat == "":

                self.errors.append(
                    f"Stap '{row['ID']}' heeft geen resultaat."
                )

    # --------------------------------------------------
    # Lege tekst
    # --------------------------------------------------

    def check_text(self):

        for row in self.rows:

            if row["TEKST"].strip() == "":

                self.errors.append(
                    f"Stap '{row['ID']}' heeft geen tekst."
                )

    # --------------------------------------------------
    # Lege optie
    # --------------------------------------------------

    def check_option(self):

        for row in self.rows:

            if row["OPTIE"].strip() == "":

                self.errors.append(
                    f"Stap '{row['ID']}' heeft geen optie."
                )

    # --------------------------------------------------
    # Dubbele resultaten
    # --------------------------------------------------

    def check_duplicate_results(self):

        results = {}

        for row in self.rows:

            result = row["RESULTAAT"].strip()

            if result == "":
                continue

            results.setdefault(
                result,
                []
            ).append(row["ID"])

        for result, ids in results.items():

            if len(ids) > 1:

                self.warnings.append(
                    f"Resultaat '{result}' komt {len(ids)} keer voor."
                )

    # --------------------------------------------------
    # Onbereikbare stappen
    # --------------------------------------------------

    def check_unreachable(self):

        reachable = {"stap_1"}

        for row in self.rows:

            next_step = row["VOLGENDE"].strip()

            if next_step != "":

                reachable.add(next_step)

        for step in self.ids:

            if step not in reachable:

                self.warnings.append(
                    f"Stap '{step}' wordt nergens gebruikt."
                )

    # --------------------------------------------------
    # Statistieken
    # --------------------------------------------------

    def get_statistics(self):

        results = 0

        for row in self.rows:

            if row["RESULTAAT"].strip():

                results += 1

        return {

            "steps": len(self.ids),

            "results": results

        }

    # --------------------------------------------------
    # Valideren
    # --------------------------------------------------

    def validate(self):

        self.errors.clear()

        self.warnings.clear()

        if not self.load():

            return False

        self.check_duplicate_ids()

        self.check_start()

        self.check_next_steps()

        self.check_results()

        self.check_text()

        self.check_option()

        self.check_duplicate_results()

        self.check_unreachable()

        return True


# ======================================================
# Test
# ======================================================

if __name__ == "__main__":

    validator = CSVValidator(
        "data/determination/Odonata.csv"
    )

    if validator.validate():

        stats = validator.get_statistics()

        print("=" * 50)
        print(" CSV VALIDATOR")
        print("=" * 50)
        print()

        print(f"Bestand      : {validator.filename}")
        print(f"Stappen      : {stats['steps']}")
        print(f"Resultaten   : {stats['results']}")
        print()

        if validator.errors:

            print("FOUTEN")
            print("-" * 50)

            for error in validator.errors:

                print(f"❌ {error}")

            print()

        else:

            print("✅ Geen fouten gevonden.\n")

        if validator.warnings:

            print("WAARSCHUWINGEN")
            print("-" * 50)

            for warning in validator.warnings:

                print(f"⚠ {warning}")

        else:

            print("✅ Geen waarschuwingen.")
