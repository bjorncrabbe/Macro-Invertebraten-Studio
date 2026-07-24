from dataclasses import dataclass


@dataclass
class ExcelNode:
    coordinate: str
    row: int
    column: int
    text: str
    node_type: str