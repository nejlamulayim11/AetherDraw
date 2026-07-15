import cv2

from app.camera import Camera
from app.config import WINDOW_NAME


def main():

    camera = Camera()

    while True:

        frame = camera.read()

        if frame is None:
            break

        cv2.imshow(WINDOW_NAME, frame)

        key = cv2.waitKey(1)

        if key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()