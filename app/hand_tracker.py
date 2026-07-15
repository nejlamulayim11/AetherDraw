import cv2
import mediapipe as mp

from app.config import (
    MAX_NUM_HANDS,
    MIN_DETECTION_CONFIDENCE,
    MIN_TRACKING_CONFIDENCE
)

from app.models import HandData, FingerState


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
        return self.hands.process(rgb)

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

    def _finger_states(self, landmarks):

        fingers = FingerState()

        fingers.thumb = landmarks[4][1] > landmarks[3][1]
        fingers.index = landmarks[8][2] < landmarks[6][2]
        fingers.middle = landmarks[12][2] < landmarks[10][2]
        fingers.ring = landmarks[16][2] < landmarks[14][2]
        fingers.pinky = landmarks[20][2] < landmarks[18][2]

        return fingers

    def get_hand(self, frame, results):

        if not results.multi_hand_landmarks:
            return None

        h, w, _ = frame.shape

        hand = results.multi_hand_landmarks[0]

        landmarks = []

        for idx, lm in enumerate(hand.landmark):

            x = int(lm.x * w)
            y = int(lm.y * h)

            landmarks.append((idx, x, y))

        handedness = "Right"

        if results.multi_handedness:
            handedness = results.multi_handedness[0].classification[0].label

        fingers = self._finger_states(landmarks)

        return HandData(

            landmarks=landmarks,

            wrist=(landmarks[0][1], landmarks[0][2]),

            thumb_tip=(landmarks[4][1], landmarks[4][2]),

            index_tip=(landmarks[8][1], landmarks[8][2]),

            middle_tip=(landmarks[12][1], landmarks[12][2]),

            ring_tip=(landmarks[16][1], landmarks[16][2]),

            pinky_tip=(landmarks[20][1], landmarks[20][2]),

            fingers=fingers,

            is_left=(handedness == "Left"),

            is_right=(handedness == "Right")
        )