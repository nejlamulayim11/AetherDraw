import cv2

from app.config import (
    CAMERA_INDEX,
    FRAME_WIDTH,
    FRAME_HEIGHT
)


class Camera:

    def __init__(self):
        self.cap = cv2.VideoCapture(CAMERA_INDEX)

        if not self.cap.isOpened():
            raise RuntimeError("Camera could not be opened.")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    def read(self):
        success, frame = self.cap.read()

        if not success:
            return None

        # Kamerayı ayna görünümüne çevir
        frame = cv2.flip(frame, 1)

        return frame

    def release(self):
        self.cap.release()