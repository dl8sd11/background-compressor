import cv2
import argparse
from utils import get_streams_name


class Splitter:
    def __init__(self, input_file, mask_file):
        raw = cv2.VideoCapture(input_file)
        mask = cv2.VideoCapture(mask_file)
        assert (self._get_size(raw) == self._get_size(mask))
        assert (raw.get(cv2.CAP_PROP_FPS) == mask.get(cv2.CAP_PROP_FPS))
        width, height = self._get_size(raw)
        fps = int(raw.get(cv2.CAP_PROP_FPS))
        print(f"Width: {width}, Height: {height}, FPS: {fps}")
        fourcc = cv2.VideoWriter_fourcc(*"XVID")

        stream_name = get_streams_name(input_file)
        fg_video = cv2.VideoWriter(stream_name["fg"], fourcc,
                                   fps, (width, height))
        bg_video = cv2.VideoWriter(stream_name["bg"], fourcc,
                                   fps, (width, height))

        while True:
            ret1, raw_frame = raw.read()
            ret2, mask_frame = mask.read()

            if not ret1 or not ret2:
                break

            gray_mask = cv2.cvtColor(mask_frame, cv2.COLOR_BGR2GRAY)
            _, binary_mask = cv2.threshold(
                gray_mask, 128, 255, cv2.THRESH_BINARY)
            inverted_mask = cv2.bitwise_not(binary_mask)
            masked_frame = cv2.bitwise_and(
                raw_frame, raw_frame, mask=binary_mask)
            bg_frame = cv2.bitwise_and(
                raw_frame, raw_frame, mask=inverted_mask)

            # Write the combined frame to the fg_video video
            fg_video.write(masked_frame)
            bg_video.write(bg_frame)

        # Release the resources
        raw.release()
        mask.release()
        fg_video.release()
        bg_video.release()
        cv2.destroyAllWindows()

    def _get_size(self, cap) -> [int, int]:
        return (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))


def main(input_file, mask_file):
    print("Splitting the input file...")
    print(f"Input file: {input_file}")
    print(f"Mask file: {mask_file}")

    splitter = Splitter(input_file, mask_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Split the video using a mask video.')
    parser.add_argument('input', type=str, help='Input file name')
    parser.add_argument('mask', type=str, help='Mask file name')
    args = parser.parse_args()
    input_file = args.input
    mask_file = args.mask
    main(input_file, mask_file)
