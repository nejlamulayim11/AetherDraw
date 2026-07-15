import cv2
import mediapipe as mp

from app.config import (
    MAX_NUM_HANDS,
    MIN_DETECTION_CONFIDENCE,
    MIN_TRACKING_CONFIDENCE
)


class HandTracker:

    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=MAX_NUM_HANDS,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE
        )

    def process(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        return results

    def draw_landmarks(self, frame, results):
        if not results.multi_hand_landmarks:
            return frame

        for hand in results.multi_hand_landmarks:
            self.mp_draw.draw_landmarks(
                frame,
                hand,
                self.mp_hands.HAND_CONNECTIONS
            )

        return frame

    def get_landmarks(self, frame, results):
        """
        Returns:
            [(id, x, y), ...]
        """

        landmark_list = []

        if not results.multi_hand_landmarks:
            return landmark_list

        h, w, _ = frame.shape

        # Şimdilik sadece ilk eli kullanıyoruz
        hand = results.multi_hand_landmarks[0]

        for idx, lm in enumerate(hand.landmark):
            x = int(lm.x * w)
            y = int(lm.y * h)

            landmark_list.append((idx, x, y))

        return landmark_list