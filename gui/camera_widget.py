"""
camera_widget.py

Professionele videowidget voor OpenCV.
"""

from __future__ import annotations

import cv2

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPainter
from PySide6.QtWidgets import QWidget


class CameraWidget(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setMinimumSize(640, 480)

        self.setStyleSheet("""
            background-color:black;
            border:1px solid #444;
        """)

        self._image = None

    def show_frame(self, frame):

        if frame is None:
            return

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        h, w, ch = rgb.shape

        self._image = QImage(
            rgb.data,
            w,
            h,
            ch * w,
            QImage.Format_RGB888
        ).copy()

        self.update()

    def paintEvent(self, event):

        super().paintEvent(event)

        painter = QPainter(self)

        if self._image is None:

            painter.setPen(Qt.white)

            painter.drawText(
                self.rect(),
                Qt.AlignCenter,
                "Geen camerabeeld"
            )

            return

        image = self._image.scaled(
            self.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        x = (self.width() - image.width()) // 2
        y = (self.height() - image.height()) // 2

        painter.drawImage(x, y, image)