import cv2

from app.camera import Camera
from app.hand_tracker import HandTracker
from app.drawing_engine import DrawingEngine
from app.gesture_engine import GestureEngine
from app.smoother import PointSmoother
from app.utils import FPSCounter
from app.config import WINDOW_NAME


def main():

    camera = Camera()
    tracker = HandTracker()
    drawing = DrawingEngine()
    gesture_engine = GestureEngine()
    smoother = PointSmoother(
    smooth_factor=0.65
)
    fps_counter = FPSCounter()

    while True:

        frame = camera.read()

        if frame is None:
            break

        drawing.initialize(frame)

        results = tracker.process(frame)

        frame = tracker.draw_landmarks(frame, results)

        hand = tracker.get_hand(frame, results)

        gesture = gesture_engine.detect(hand)

        if hand:

            smooth_point = smoother.smooth(hand.index_tip)

            # İşaret parmağı ucu
            cv2.circle(
                frame,
                smooth_point,
                10,
                (0, 0, 255),
                -1
            )

            # Gesture rengi
            if gesture == GestureEngine.DRAW:
                gesture_color = (0, 255, 0)

            elif gesture == GestureEngine.ERASE:
                gesture_color = (0, 0, 255)

            else:
                gesture_color = (255, 255, 255)

            # Gesture bilgisi
            cv2.putText(
                frame,
                f"Gesture : {gesture}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                gesture_color,
                2
            )

            # Parmağın koordinatı
            cv2.putText(
                frame,
                f"Point : {smooth_point}",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )

            # Çizim
            if gesture == GestureEngine.DRAW:

                drawing.draw(smooth_point)

            elif gesture == GestureEngine.ERASE:

                drawing.erase(smooth_point)

            else:

                drawing.draw(None)

        else:

            smoother.smooth(None)
            drawing.draw(None)

            cv2.putText(
                frame,
                "Gesture : IDLE",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

        # Çizim katmanını kameraya ekle
        frame = drawing.merge(frame)

        # FPS
        fps = fps_counter.update()

        cv2.putText(
            frame,
            f"FPS : {fps}",
            (20, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 0, 0),
            2
        )

        # Yardım metni
        cv2.putText(
            frame,
            "Draw  : Index Finger",
            (20, 145),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "Erase : Index + Middle",
            (20, 170),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2
        )

        cv2.putText(
            frame,
            "C : Clear    Q : Quit",
            (20, 195),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.imshow(WINDOW_NAME, frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("c"):
            drawing.clear()

        elif key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()