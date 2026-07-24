"""
count_manager.py

Beheer van de tellingen per familie en genus.
"""


class CountManager:

    def __init__(self):

        self.counts = {}

    def add(self, family, genus):

        key = (family, genus)

        if key not in self.counts:
            self.counts[key] = 0

        self.counts[key] += 1

    def remove(self, family, genus):

        key = (family, genus)

        if key not in self.counts:
            return

        if self.counts[key] > 0:
            self.counts[key] -= 1

        if self.counts[key] == 0:
            del self.counts[key]

    def get_total(self):

        return sum(self.counts.values())

    def get_all(self):

        return self.counts
