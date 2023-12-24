import cv2
import argparse
from utils import get_streams_name


def main(foreground, background):
    fg_stream = cv2.VideoCapture(foreground)
    bg_stream = cv2.VideoCapture(background)
    while True:
        ret1, fg_frame = fg_stream.read()
        ret2, bg_frame = bg_stream.read()

        if not ret1 or not ret2:
            break

        sum_frame = cv2.add(fg_frame, bg_frame).clip(0, 255)
        cv2.imshow("Player", sum_frame)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break

        if key == ord('p'):
            while True:
                back = cv2.waitKey(-1)
                if back == ord('p'):
                    break

    fg_stream.release()
    bg_stream.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Play the compressed video')
    parser.add_argument('fg', type=str, help='Foreground file name')
    parser.add_argument('bg', type=str, help='Background file name')
    args = parser.parse_args()
    foreground = args.fg
    background = args.bg
    main(foreground, background)
