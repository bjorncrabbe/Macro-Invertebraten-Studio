"""
new_sample_dialog.py

Dialoog voor het starten van een nieuw of bestaand staal.
"""

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QRadioButton,
    QVBoxLayout,
)


class NewSampleDialog(QDialog):

    def __init__(self, operators, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Nieuw staal")

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.meetpunt_edit = QLineEdit()

        self.meetpunt_edit.setPlaceholderText("123456")

        self.meetpunt_edit.setMaxLength(6)

        self.operator_combo = QComboBox()

        for operator in operators:

            self.operator_combo.addItem(
                operator["name"],
                operator["id"]
            )

        self.new_radio = QRadioButton("Nieuw staal")
        self.new_radio.setChecked(True)

        self.open_radio = QRadioButton("Bestaand staal openen")

        form.addRow(
            "Meetpunt:",
            self.meetpunt_edit
        )
        form.addRow("Operator:", self.operator_combo)

        layout.addLayout(form)

        layout.addWidget(self.new_radio)
        layout.addWidget(self.open_radio)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)