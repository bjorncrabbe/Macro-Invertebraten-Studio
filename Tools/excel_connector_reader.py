import xml.etree.ElementTree as ET
import zipfile

from excel_connector import ExcelConnector


class ExcelConnectorReader:

    def __init__(self, excel_file):

        self.excel_file = excel_file

        self.connectors = []

    def load(self, drawing_path):

        self.connectors.clear()

        with zipfile.ZipFile(self.excel_file) as z:

            root = ET.fromstring(
                z.read(drawing_path)
            )

        ns = {
            "xdr": "http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing",
            "a": "http://schemas.openxmlformats.org/drawingml/2006/main"
        }

        for anchor in root.findall("xdr:twoCellAnchor", ns):

            connector = anchor.find("xdr:cxnSp", ns)

            if connector is None:
                continue

            start = anchor.find("xdr:from", ns)
            end = anchor.find("xdr:to", ns)

            start_col = int(start.find("xdr:col", ns).text)
            start_row = int(start.find("xdr:row", ns).text)

            end_col = int(end.find("xdr:col", ns).text)
            end_row = int(end.find("xdr:row", ns).text)

            shape = connector.find("xdr:spPr/a:prstGeom", ns)

            if shape is None:
                shape_type = "unknown"
            else:
                shape_type = shape.attrib["prst"]

            self.connectors.append(

                ExcelConnector(

                    start_row=start_row,
                    start_col=start_col,

                    end_row=end_row,
                    end_col=end_col,

                    shape_type=shape_type
                )
            )
if __name__ == "__main__":

    import os

    BASE_DIR = os.path.dirname(
        os.path.dirname(__file__)
    )

    EXCEL_FILE = os.path.join(
        BASE_DIR,
        "Data",
        "Determination",
        "excel",
        "DeterminatiesleutelMacroinvertebraten.xlsx"
    )

    reader = ExcelConnectorReader(
        EXCEL_FILE
    )

    reader.load(
        "xl/drawings/drawing9.xml"
    )

    print()

    print(f"{len(reader.connectors)} connectors gevonden\n")

    for connector in reader.connectors:

        print(
            f"({connector.start_row},{connector.start_col})"
            f" -> "
            f"({connector.end_row},{connector.end_col})"
            f"    "
            f"{connector.shape_type}"
        )