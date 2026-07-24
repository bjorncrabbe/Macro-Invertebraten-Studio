from dataclasses import dataclass


@dataclass
class ExcelShape:

    id: int

    name: str

    row: int
    col: int

    text: str