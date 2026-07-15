import cv2

from app.camera import Camera
from app.hand_tracker import HandTracker
from app.drawing_engine import DrawingEngine
from app.utils import FPSCounter
from app.config import WINDOW_NAME


def main():

    camera = Camera()
    tracker = HandTracker()
    drawing = DrawingEngine()
    fps_counter = FPSCounter()

    while True:

        frame = camera.read()

        if frame is None:
            print("Failed to capture frame.")
            break

        # Hand Detection
        results = tracker.process(frame)

        # Draw Hand Skeleton
        frame = tracker.draw_landmarks(frame, results)

        # Get Landmarks
        landmarks = tracker.get_landmarks(frame, results)

        if landmarks:

            _, x, y = landmarks[8]

            # Draw on canvas
            drawing.draw((x, y))

            # Show fingertip
            cv2.circle(
                frame,
                (x, y),
                10,
                (0, 0, 255),
                -1
            )

            # Coordinates
            cv2.putText(
                frame,
                f"Index Finger : ({x}, {y})",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        else:

            drawing.draw(None)

        # Merge drawing canvas with camera image
        frame = drawing.merge(frame)

        # FPS
        fps = fps_counter.update()

        cv2.putText(
            frame,
            f"FPS : {fps}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 0),
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