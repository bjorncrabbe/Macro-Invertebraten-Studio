"""
screenshot.py

Opslaan van camerabeelden.
"""

import os
from datetime import datetime

import cv2

from config import SCREENSHOT_FOLDER


class ScreenshotManager:

    def __init__(self):

        os.makedirs(
            SCREENSHOT_FOLDER,
            exist_ok=True
        )

    def save(self, frame):

        now = datetime.now()

        filename = now.strftime(
            "IMG_%Y%m%d_%H%M%S.png"
        )

        path = os.path.join(
            SCREENSHOT_FOLDER,
            filename
        )

        cv2.imwrite(path, frame)

        return filename