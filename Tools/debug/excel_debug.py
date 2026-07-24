import zipfile
import xml.etree.ElementTree as ET

EXCEL_FILE = r"/Data/Determination/excel/DeterminatiesleutelMacroinvertebraten.xlsx"

ns = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships"
}

with zipfile.ZipFile(EXCEL_FILE) as z:

    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))

    print("\nWorkbook relaties:\n")

    for rel in rels:
        print(
            rel.attrib["Id"],
            "->",
            rel.attrib["Target"]
        )