"""
app.py

Hoofdvenster van Macro-Invertebraten Studio.
"""

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QMainWindow,
    QWidget,
)

from controllers.app_controller import AppController

from gui.camera_widget import CameraWidget
from gui.dialogs.new_sample_dialog import NewSampleDialog
from gui.side_panel import SidePanel


class MacroStudio(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Macro-Invertebraten Studio v1.0"
        )

        self.resize(1400, 850)

        # Controller
        self.controller = AppController()

        # Welke determinatiesleutel is momenteel actief?
        self.current_key = None

        # Laatste AI-label
        self.ai_label = None
        self.ai_confidence = 0.0

        # AI slechts enkele keren per seconde
        self.ai_counter = 0

        # Eerst een staal kiezen
        if not self.start_sample():

            self.close()

            return

        # GUI opbouwen
        self.build_ui()

        # Camera starten
        self.start_camera()

        # Timer starten
        self.start_timer()

        # Eerste sleutel tonen
        self.update_key_panel()

        self.side_panel.plus_button.clicked.connect(
            self.add_observation
        )

        self.side_panel.minus_button.clicked.connect(
            self.remove_observation
        )

        self.side_panel.keep_key_button.clicked.connect(
            self.keep_current_key
        )

        self.side_panel.use_ai_button.clicked.connect(
            self.use_ai_key
        )

    def start_sample(self):

        operators = self.controller.operators.get_active()

        dialog = NewSampleDialog(
            operators,
            self
        )

        if dialog.exec() != QDialog.Accepted:
            return False

        meetpunt = dialog.meetpunt_edit.text()

        operator_id = dialog.operator_combo.currentData()

        if dialog.new_radio.isChecked():

            self.controller.new_sample(
                meetpunt,
                operator_id
            )

        else:

            if not self.controller.open_sample(
                meetpunt
            ):
                raise RuntimeError(
                    "Staal niet gevonden."
                )

        return True

    def build_ui(self):

        central = QWidget()

        self.setCentralWidget(central)

        layout = QHBoxLayout(central)

        self.camera_widget = CameraWidget()

        layout.addWidget(
            self.camera_widget,
            stretch=3
        )

        self.side_panel = SidePanel()

        self.side_panel.reset_button.clicked.connect(
            self.reset_key
        )

        layout.addWidget(
            self.side_panel,
            stretch=1
        )

    def start_camera(self):

        if not self.controller.start_camera():

            raise RuntimeError(
                "Geen camera gevonden."
            )

    def start_timer(self):

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.update_camera
        )

        self.timer.start(33)

    def update_camera(self):

        frame = self.controller.get_frame()

        if frame is None:
            return

        # Camerabeeld tonen
        self.camera_widget.show_frame(frame)

        # AI niet op elk frame uitvoeren
        self.ai_counter += 1

        if self.ai_counter < 6:
            return

        self.ai_counter = 0

        # AI voorspelling
        label, confidence = self.controller.predict(frame)

        print("=" * 40)
        print("AI label:", label)
        print("Confidence:", confidence)

        if label is None:
            return

        # Laatste AI-waarneming bewaren
        self.ai_label = label
        self.ai_confidence = confidence

        # AI altijd tonen
        self.side_panel.set_ai_prediction(
            label,
            confidence
        )

        # Alleen verder bij voldoende zekerheid
        if confidence < 90:
            return

        key_name = label.lower()

        print(
            f"AI={label} | "
            f"key={key_name} | "
            f"current={self.current_key}"
        )

        # Controleer of er een determinatiesleutel bestaat
        available = [
            key.lower()
            for key in self.controller.get_available_keys()
        ]

        if key_name not in available:

            self.side_panel.clear_key_conflict()

            self.side_panel.set_result(
                "⚠ Geen determinatiesleutel beschikbaar."
            )

            return

        # --------------------------------------------------
        # GEEN actieve sleutel:
        # de eerste betrouwbare AI-predictie mag de
        # determinatiesleutel openen.
        # --------------------------------------------------

        if self.current_key is None:

            print(
                "Nog geen actieve sleutel."
            )

            print(
                "Nieuwe sleutel laden:",
                key_name
            )

            if not self.controller.load_key(key_name):

                self.side_panel.set_result(
                    "⚠ Geen determinatiesleutel beschikbaar."
                )

                return

            self.current_key = key_name

            self.side_panel.clear_key_conflict()

            self.update_key_panel()

            print(
                "Actieve sleutel:",
                self.current_key
            )

            return

        # --------------------------------------------------
        # Er is al een actieve sleutel.
        #
        # Een afwijkende AI-predictie mag de sleutel NIET
        # automatisch vervangen.
        # --------------------------------------------------

        if key_name != self.current_key:

            print(
                "AI voorspelling wijkt af van "
                "de actieve determinatiesleutel."
            )

            print(
                f"Actieve sleutel: {self.current_key}"
            )

            print(
                f"Nieuwe AI voorspelling: {key_name}"
            )

            self.side_panel.show_key_conflict(
                self.current_key,
                label,
                confidence
            )

            return

        # AI en huidige sleutel komen overeen.
        self.side_panel.clear_key_conflict()

    def keep_current_key(self):

        if self.current_key is None:
            return

        print(
            "Huidige determinatiesleutel behouden:",
            self.current_key
        )

        self.side_panel.clear_key_conflict()

        # Zorg dat de huidige opties zichtbaar blijven.
        self.update_key_panel()

    def use_ai_key(self):

        if self.ai_label is None:
            return

        key_name = self.ai_label.lower()

        available = [
            key.lower()
            for key in self.controller.get_available_keys()
        ]

        if key_name not in available:
            self.side_panel.set_result(
                "⚠ Geen determinatiesleutel beschikbaar."
            )
            return

        print(
            "Gebruiker kiest AI-determinatiesleutel:",
            key_name
        )

        if not self.controller.load_key(key_name):
            self.side_panel.set_result(
                "⚠ Geen determinatiesleutel beschikbaar."
            )
            return

        self.current_key = key_name

        self.side_panel.clear_key_conflict()

        self.update_key_panel()

    def update_key_panel(self):

        print(
            "====== update_key_panel ======"
        )

        options = self.controller.get_options()

        print(options)

        if options is None:
            return

        print(
            "roep set_options aan"
        )

        self.side_panel.set_options(
            options,
            self.handle_choice
        )

        print("klaar")

    def handle_choice(self, option):

        finished, result = self.controller.choose(
            option
        )

        print(
            "Finished:",
            finished
        )

        print(
            "Result:",
            result
        )

        print(
            "Current step:",
            self.controller.key.current_step
        )

        if finished:

            self.side_panel.set_result(
                result
            )

        else:

            self.update_key_panel()

    def reset_key(self):

        self.controller.reset_key()

        # Na reset mag de volgende betrouwbare AI-predictie
        # opnieuw een sleutel openen.
        self.current_key = None

        self.ai_label = None
        self.ai_confidence = 0.0

        self.side_panel.clear_key_conflict()

        self.side_panel.set_result(
            "Nog geen resultaat."
        )

        self.update_key_panel()

    def add_observation(self):

        print("PLUS")

        family = (
            self.side_panel.family_label.text()
        )

        genus = self.controller.get_result()

        print(
            family,
            genus
        )

        self.controller.add_count(
            family,
            genus
        )

        print(
            self.controller.get_total_count()
        )

        self.side_panel.set_count(
            self.controller.get_total_count()
        )

    def remove_observation(self):

        family = (
            self.side_panel.family_label.text()
        )

        genus = self.controller.get_result()

        if genus is None:
            return

        self.controller.remove_count(
            family,
            genus
        )

        self.side_panel.set_count(
            self.controller.get_total_count()
        )

    def closeEvent(self, event):

        if hasattr(self, "timer"):
            self.timer.stop()

        self.controller.stop_camera()

        event.accept()
