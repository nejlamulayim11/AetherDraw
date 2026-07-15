import cv2
import numpy as np


class DrawingEngine:

    def __init__(self, width=1280, height=720):

        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)

        self.previous_point = None

        self.color = (0, 255, 0)

        self.thickness = 5

    def draw(self, point):

        if point is None:
            self.previous_point = None
            return

        if self.previous_point is None:
            self.previous_point = point
            return

        cv2.line(
            self.canvas,
            self.previous_point,
            point,
            self.color,
            self.thickness
        )

        self.previous_point = point

    def merge(self, frame):

        return cv2.add(frame, self.canvas)

    def clear(self):

        self.canvas[:] = 0