import cv2

from config import (
    CAMERA_WIDTH,
    CAMERA_HEIGHT,
    CAMERA_FPS
)


class Camera:

    def __init__(self):

        self.cap = None
        self.index = None

    def connect(self):

        self.disconnect()

        for camera in range(6):

            cap = cv2.VideoCapture(camera, cv2.CAP_DSHOW)

            if not cap.isOpened():
                cap.release()
                cap = cv2.VideoCapture(camera, cv2.CAP_MSMF)

            if cap.isOpened():

                cap.set(
                    cv2.CAP_PROP_FOURCC,
                    cv2.VideoWriter_fourcc(*"MJPG")
                )

                cap.set(
                    cv2.CAP_PROP_FRAME_WIDTH,
                    CAMERA_WIDTH
                )

                cap.set(
                    cv2.CAP_PROP_FRAME_HEIGHT,
                    CAMERA_HEIGHT
                )

                cap.set(
                    cv2.CAP_PROP_FPS,
                    CAMERA_FPS
                )

                self.cap = cap
                self.index = camera

                print(f"Camera gevonden op poort {camera}")

                return True

        return False

    def read(self):

        if self.cap is None:
            return None

        ok, frame = self.cap.read()

        if not ok:
            return None

        return frame

    def disconnect(self):

        if self.cap is not None:

            self.cap.release()
            self.cap = None

    def reconnect(self):

        self.disconnect()
        return self.connect()