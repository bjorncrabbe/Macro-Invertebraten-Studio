import os
import zipfile
import xml.etree.ElementTree as ET

from Excel_key_reader import ExcelKeyReader
from excel_connector_reader import ExcelConnectorReader


class ExcelImporter:

    def __init__(self, excel_file):

        self.excel_file = excel_file

        self.key_reader = ExcelKeyReader(excel_file)
        self.connector_reader = ExcelConnectorReader(excel_file)

    def get_drawing_path(self, sheet_name):
        """
        Zoek automatisch de drawing.xml die bij een werkblad hoort.
        """

        ns_main = {
            "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
        }

        with zipfile.ZipFile(self.excel_file) as z:

            workbook = ET.fromstring(
                z.read("xl/workbook.xml")
            )

            workbook_rels = ET.fromstring(
                z.read("xl/_rels/workbook.xml.rels")
            )

            sheet_rid = None

            sheets = workbook.find("main:sheets", ns_main)

            for sheet in sheets:

                if sheet.attrib["name"] == sheet_name:

                    sheet_rid = sheet.attrib[
                        "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
                    ]

                    break

            if sheet_rid is None:
                raise ValueError(f"Werkblad '{sheet_name}' niet gevonden.")

            sheet_target = None

            for rel in workbook_rels:

                if rel.attrib["Id"] == sheet_rid:

                    sheet_target = rel.attrib["Target"]

                    break

            if sheet_target is None:
                raise ValueError("Sheet xml niet gevonden.")

            sheet_xml = sheet_target.split("/")[-1]

            rel_path = f"xl/worksheets/_rels/{sheet_xml}.rels"

            sheet_rels = ET.fromstring(
                z.read(rel_path)
            )

            for rel in sheet_rels:

                target = rel.attrib.get("Target", "")

                if "drawing" in target:

                    target = target.replace("../", "")

                    return f"xl/{target}"

        raise ValueError(f"Geen drawing gevonden voor '{sheet_name}'.")

    def find_nearest_node(self, row, col):
        """
        Zoek de node die het dichtst bij een bepaalde positie ligt.
        """

        closest = None
        best_distance = float("inf")

        for node in self.key_reader.nodes:

            distance = abs(node.row - row) + abs(node.column - col)

            if distance < best_distance:

                best_distance = distance
                closest = node

        return closest

    def analyze_connectors(self, radius=2):
        """
        Toon voor elke connector welke nodes in de buurt liggen.
        """

        print("\n========== CONNECTOR ANALYSE ==========\n")

        for i, connector in enumerate(self.connector_reader.connectors, start=1):

            print(f"Connector {i}")
            print(f"  Start : ({connector.start_row}, {connector.start_col})")
            print(f"  Eind  : ({connector.end_row}, {connector.end_col})")

            print("  Mogelijke startnodes:")

            for node in self.key_reader.nodes:

                if (
                        abs(node.row - connector.start_row) <= radius
                        and
                        abs(node.column - connector.start_col) <= radius
                ):
                    print(
                        f"    {node.coordinate:<4}"
                        f"{node.node_type:<10}"
                        f"({node.row},{node.column})"
                    )

            print()

            print("  Mogelijke eindnodes:")

            for node in self.key_reader.nodes:

                if (
                        abs(node.row - connector.end_row) <= radius
                        and
                        abs(node.column - connector.end_col) <= radius
                ):
                    print(
                        f"    {node.coordinate:<4}"
                        f"{node.node_type:<10}"
                        f"({node.row},{node.column})"
                    )

            print("-" * 60)

    def convert(self, sheet_name):

        print(f"Importeren van {sheet_name}")

        # Nodes lezen
        self.key_reader.open(sheet_name)
        self.key_reader.read_nodes()

        # Drawing zoeken
        drawing = self.get_drawing_path(sheet_name)

        print(f"Drawing gevonden: {drawing}")

        # Connectoren lezen
        self.connector_reader.load(drawing)

        print(f"{len(self.key_reader.nodes)} nodes gevonden")
        print(f"{len(self.connector_reader.connectors)} connectors gevonden")

        node_lookup = {
            (node.row, node.column): node
            for node in self.key_reader.nodes
        }

        print("\n========== EXACTE MATCHES ==========\n")

        for connector in self.connector_reader.connectors:
            start = node_lookup.get(
                (connector.start_row, connector.start_col)
            )

            end = node_lookup.get(
                (connector.end_row, connector.end_col)
            )

            print(
                f"({connector.start_row},{connector.start_col})"
                f" -> "
                f"({connector.end_row},{connector.end_col})"
            )

            print(
                "   START:",
                start.coordinate if start else "GEEN",
                "-",
                start.text if start else ""
            )

            print(
                "   EINDE:",
                end.coordinate if end else "GEEN",
                "-",
                end.text if end else ""
            )

            print()
        print("\n========== NODES ==========\n")

        for node in self.key_reader.nodes:
            print(
                f"{node.coordinate:4} "
                f"({node.row},{node.column}) "
                f"{node.text}"
            )

if __name__ == "__main__":

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

    importer = ExcelImporter(EXCEL_FILE)

    importer.convert("HIRUDINEA")