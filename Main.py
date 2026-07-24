import sys

from PySide6.QtWidgets import QApplication

from gui.app import MacroStudio


def main():

    app = QApplication(sys.argv)

    window = MacroStudio()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":

    main()