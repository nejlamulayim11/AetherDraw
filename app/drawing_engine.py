import cv2
import numpy as np


class DrawingEngine:

    def __init__(self):

        self.canvas = None
        self.previous_point = None

        # BGR renk
        self.draw_color = (255, 255, 255)

        self.erase_color = (0, 0, 0)

        # Daha rahat yazı için
        self.draw_size = 5
        self.erase_size = 50


    def initialize(self, frame):

        if self.canvas is None:

            h, w, _ = frame.shape

            self.canvas = np.zeros(
                (h, w, 3),
                dtype=np.uint8
            )


    def draw(self, point):

        self._paint(
            point,
            self.draw_color,
            self.draw_size
        )


    def erase(self, point):

        self._paint(
            point,
            self.erase_color,
            self.erase_size
        )


    def _paint(self, point, color, thickness):

        if self.canvas is None:
            return


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
            color,
            thickness,
            cv2.LINE_AA
        )


        # küçük hareketlerde yumuşaklık
        cv2.circle(
            self.canvas,
            point,
            thickness // 2,
            color,
            -1
        )


        self.previous_point = point



    def merge(self, frame):

        if self.canvas is None:
            return frame


        return cv2.add(
            frame,
            self.canvas
        )


    def clear(self):

        if self.canvas is not None:

            self.canvas[:] = 0

            self.previous_point = None