import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from backend.camera import Camera
from gui.camera_widget import CameraWidget

app = QApplication(sys.argv)

camera = Camera()

if not camera.connect():
    raise RuntimeError("Camera kon niet worden geopend.")

window = CameraWidget()
window.resize(900, 600)
window.show()


def update():

    frame = camera.read()

    window.show_frame(frame)


timer = QTimer()
timer.timeout.connect(update)
timer.start(30)


exit_code = app.exec()

camera.disconnect()

sys.exit(exit_code)