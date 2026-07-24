
"""
operators.py

Beheer van de operators.
"""

from __future__ import annotations

import json
import os

from config import OPERATORS_FILE

class OperatorManager:

    def __init__(self):

        self.data = {}

        self.load()

    def load(self):
        if not os.path.exists(OPERATORS_FILE):
            self.data = {

                "version": 1,

                "last_operator": None,

                "operators": []

            }

            self.save()

            return
        with open(
            OPERATORS_FILE,
            "r",
            encoding="utf8"
        ) as file:

            self.data = json.load(file)

    def save(self):

        with open(
            OPERATORS_FILE,
            "w",
            encoding="utf8"
        ) as file:

            json.dump(
                self.data,
                file,
                indent=4
            )

    def get_active(self):

        return sorted(

            [

                operator

                for operator in self.data["operators"]

                if operator["active"]

            ],

            key=lambda operator: operator["name"]

        )

    def add(self, name, initials):

        name = name.strip()
        initials = initials.strip().upper()

        if not name:
            raise ValueError("Naam mag niet leeg zijn.")

        if not initials:
            raise ValueError("Initialen mogen niet leeg zijn.")

        for operator in self.data["operators"]:

            if operator["name"].lower() == name.lower():
                raise ValueError("Operator bestaat al.")

            if operator["initials"].upper() == initials:
                raise ValueError("Initialen bestaan al.")

        new_id = max(
            (operator["id"] for operator in self.data["operators"]),
            default=0
        ) + 1

        self.data["operators"].append({

            "id": new_id,

            "name": name,

            "initials": initials,

            "active": True

        })

        self.save()

    def deactivate(self, operator_id):

        for operator in self.data["operators"]:

            if operator["id"] == operator_id:
                operator["active"] = False

                self.save()

                return True

        return False

    def get_by_id(self, operator_id):

        for operator in self.data["operators"]:

            if operator["id"] == operator_id:
                return operator

        return None

    def get_last_used(self):

        return self.data.get("last_operator")

    def set_last_used(self, operator_id):

        if self.get_by_id(operator_id) is None:
            return False

        self.data["last_operator"] = operator_id

        self.save()

        return True

    def exists(self, name, initials):

        for operator in self.data["operators"]:

            if operator["name"].lower() == name.lower():
                 return True

            if operator["initials"].upper() == initials.upper():
                return True

        return False

    def count(self):

        return len(self.get_active())

    def get_names(self):

        return [

            operator["name"]

            for operator in self.get_active()

    ]