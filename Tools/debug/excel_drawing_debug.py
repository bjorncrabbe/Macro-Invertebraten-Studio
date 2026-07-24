import os
import zipfile
import xml.etree.ElementTree as ET

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

# HIRUDINEA = sheet10.xml
SHEET = "sheet10.xml"

ns_rel = {
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships"
}

with zipfile.ZipFile(EXCEL_FILE) as z:

    print(f"\nZoek drawing van {SHEET}\n")

    rel_file = f"xl/worksheets/_rels/{SHEET}.rels"

    root = ET.fromstring(z.read(rel_file))

    drawing_target = None

    for rel in root:

        target = rel.attrib.get("Target", "")

        print(
            rel.attrib["Id"],
            rel.attrib["Type"].split("/")[-1],
            target
        )

        if "drawing" in target:
            drawing_target = target

    if drawing_target is None:
        print("\nGeen drawing gevonden.")
        quit()

    drawing_path = "xl/" + drawing_target.replace("../", "")

    print("\nDrawing bestand:")
    print(drawing_path)

    print("\n==============================\n")

    xml = z.read(drawing_path).decode("utf-8")

    print(xml[:8000])