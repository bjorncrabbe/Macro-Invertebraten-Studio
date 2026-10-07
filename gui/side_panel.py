"""
side_panel.py

Rechter bedieningspaneel van Macro-Invertebraten Studio.
"""

from functools import partial

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QGroupBox,
    QProgressBar,
)


class SidePanel(QWidget):

    def __init__(self):

        super().__init__()

        self.build_ui()

    # -----------------------------------------------------
    # GUI
    # -----------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout(self)

        layout.setSpacing(15)

        self.setMinimumWidth(340)
        self.setMaximumWidth(420)

        # =================================================
        # AI
        # =================================================

        ai_box = QGroupBox("AI Herkenning")

        ai_layout = QVBoxLayout(ai_box)

        self.family_label = QLabel("Geen voorspelling")
        self.family_label.setAlignment(Qt.AlignCenter)

        self.family_label.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
        """)

        self.confidence_label = QLabel("0.0 %")
        self.confidence_label.setAlignment(Qt.AlignCenter)

        self.confidence_bar = QProgressBar()
        self.confidence_bar.setRange(0, 100)
        self.confidence_bar.setValue(0)
        self.confidence_bar.setTextVisible(False)

        self.status_label = QLabel("⚪ AI niet actief")
        self.status_label.setAlignment(Qt.AlignCenter)

        ai_layout.addWidget(self.family_label)
        ai_layout.addWidget(self.confidence_label)
        ai_layout.addWidget(self.confidence_bar)
        ai_layout.addWidget(self.status_label)

        layout.addWidget(ai_box)

        # =================================================
        # AI / determinatieconflict
        # =================================================

        self.conflict_box = QGroupBox("AI wijkt af")

        conflict_layout = QVBoxLayout(self.conflict_box)

        self.conflict_label = QLabel("")
        self.conflict_label.setAlignment(Qt.AlignCenter)
        self.conflict_label.setWordWrap(True)

        self.use_ai_button = QPushButton(
            "AI voorspelling gebruiken"
        )

        self.keep_key_button = QPushButton(
            "Huidige sleutel behouden"
        )

        self.use_ai_button.setMinimumHeight(40)
        self.keep_key_button.setMinimumHeight(40)

        conflict_layout.addWidget(
            self.conflict_label
        )

        conflict_layout.addWidget(
            self.use_ai_button
        )

        conflict_layout.addWidget(
            self.keep_key_button
        )

        layout.addWidget(self.conflict_box)

        self.conflict_box.hide()

        # =================================================
        # Determinatiesleutel
        # =================================================

        key_box = QGroupBox("Determinatiesleutel")

        key_layout = QVBoxLayout(key_box)

        self.key_layout = key_layout

        self.option_buttons = []

        layout.addWidget(key_box)

        # =================================================
        # Resultaat
        # =================================================

        result_box = QGroupBox("Resultaat")

        result_layout = QVBoxLayout(result_box)

        self.result_label = QLabel(
            "Nog geen resultaat"
        )

        self.result_label.setAlignment(
            Qt.AlignCenter
        )

        self.result_label.setWordWrap(True)

        self.count_label = QLabel("0")

        self.count_label.setAlignment(
            Qt.AlignCenter
        )

        self.count_label.setStyleSheet("""
            font-size:30px;
            font-weight:bold;
        """)

        self.plus_button = QPushButton("+1")
        self.minus_button = QPushButton("-1")

        self.plus_button.setMinimumHeight(45)
        self.minus_button.setMinimumHeight(45)

        result_layout.addWidget(
            self.result_label
        )

        result_layout.addWidget(
            self.count_label
        )

        result_layout.addWidget(
            self.plus_button
        )

        result_layout.addWidget(
            self.minus_button
        )

        layout.addWidget(result_box)

        # =================================================
        # Algemene knoppen
        # =================================================

        self.save_button = QPushButton(
            "💾 Waarneming opslaan"
        )

        self.reset_button = QPushButton(
            "🔄 Reset sleutel"
        )

        self.save_button.setMinimumHeight(45)
        self.reset_button.setMinimumHeight(45)

        layout.addWidget(
            self.save_button
        )

        layout.addWidget(
            self.reset_button
        )

        layout.addStretch()

    # =====================================================
    # AI
    # =====================================================

    def set_ai_prediction(
        self,
        family,
        confidence
    ):

        self.family_label.setText(
            family
        )

        self.confidence_label.setText(
            f"{confidence:.1f} %"
        )

        self.confidence_bar.setValue(
            max(0, min(100, int(confidence)))
        )

        if confidence >= 90:

            self.status_label.setText(
                "🟢 Hoge betrouwbaarheid"
            )

        elif confidence >= 70:

            self.status_label.setText(
                "🟡 Redelijke betrouwbaarheid"
            )

        else:

            self.status_label.setText(
                "🔴 Lage betrouwbaarheid"
            )

    # =====================================================
    # Conflict tussen AI en actieve sleutel
    # =====================================================

    def show_key_conflict(
        self,
        current_key,
        ai_label,
        confidence
    ):

        current_name = (
            current_key.replace("_", " ").title()
        )

        self.conflict_label.setText(
            f"AI voorspelt "
            f"<b>{ai_label}</b> "
            f"({confidence:.1f}%), "
            f"maar de actieve sleutel is "
            f"<b>{current_name}</b>."
        )

        self.conflict_box.show()

    def clear_key_conflict(self):

        self.conflict_box.hide()

    # =====================================================
    # Determinatiesleutel
    # =====================================================

    def set_options(
        self,
        options,
        callback
    ):

        print("===== set_options =====")
        print(options)

        # Oude knoppen verwijderen
        for button in self.option_buttons:

            self.key_layout.removeWidget(
                button
            )

            button.setParent(None)
            button.deleteLater()

        self.option_buttons.clear()

        # Nieuwe knoppen maken
        for key, value in options.items():

            print(
                "Maak knop:",
                key
            )

            button = QPushButton(
                value["tekst"]
            )

            button.setMinimumHeight(70)

            button.clicked.connect(
                partial(
                    callback,
                    key
                )
            )

            self.key_layout.addWidget(
                button
            )

            self.option_buttons.append(
                button
            )

        print(
            "Aantal knoppen:",
            len(self.option_buttons)
        )

    # =====================================================
    # Resultaat
    # =====================================================

    def set_result(self, text):

        self.result_label.setText(
            text
        )

    def set_count(self, count):

        self.count_label.setText(
            str(count)
        )
