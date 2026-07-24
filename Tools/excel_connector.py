from dataclasses import dataclass


@dataclass
class ExcelConnector:

    start_row: int
    start_col: int

    end_row: int
    end_col: int

    shape_type: str