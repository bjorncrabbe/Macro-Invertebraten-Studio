import sys

from PySide6.QtWidgets import QApplication

from gui.side_panel import SidePanel

app = QApplication(sys.argv)

panel = SidePanel()

panel.set_ai_prediction(
    "Libellen",
    98.7
)

panel.set_options(
    "A. 3 staartdraden",
    "B. Geen staartdraden"
)

panel.set_result(
    "Nog geen eindresultaat."
)

panel.show()

sys.exit(app.exec())