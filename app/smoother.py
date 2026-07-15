class PointSmoother:

    def __init__(self, smooth_factor=0.65):

        self.previous = None
        self.smooth_factor = smooth_factor


    def smooth(self, point):

        if point is None:
            self.previous = None
            return None


        if self.previous is None:

            self.previous = point
            return point


        x = int(
            self.previous[0] * self.smooth_factor +
            point[0] * (1 - self.smooth_factor)
        )

        y = int(
            self.previous[1] * self.smooth_factor +
            point[1] * (1 - self.smooth_factor)
        )


        self.previous = (x, y)

        return (x, y)