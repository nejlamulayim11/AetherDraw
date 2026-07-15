class GestureEngine:

    DRAW = "DRAW"
    ERASE = "ERASE"
    IDLE = "IDLE"

    def detect(self, hand):

        if hand is None:
            return self.IDLE

        fingers = hand.fingers

        if (
            fingers.index
            and not fingers.middle
            and not fingers.ring
            and not fingers.pinky
        ):
            return self.DRAW

        if (
            fingers.index
            and fingers.middle
            and not fingers.ring
            and not fingers.pinky
        ):
            return self.ERASE

        return self.IDLE