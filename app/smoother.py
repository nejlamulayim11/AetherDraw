from collections import deque


class PointSmoother:

    def __init__(self, window_size=5):
        self.points = deque(maxlen=window_size)

    def smooth(self, point):

        if point is None:
            self.points.clear()
            return None

        self.points.append(point)

        avg_x = sum(p[0] for p in self.points) // len(self.points)
        avg_y = sum(p[1] for p in self.points) // len(self.points)

        return (avg_x, avg_y)