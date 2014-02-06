"""
Dependencies:

- OpenCV >= 2.4.4
"""

import sys

import numpy as np
import cv2


DEBUG = True


# http://stackoverflow.com/questions/10948589/choosing-correct-hsv-values-for-opencv-thresholding-with-inranges

# The HSV value range that is used to get green color of the image
GREEN_RANGE_MIN = np.array([50, 70, 70], np.uint8)
GREEN_RANGE_MAX = np.array([75, 255, 255], np.uint8)


def find_color(image, min_hsv, max_hsv):
    """Returns black and white image where green color is white."""
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv_image, min_hsv, max_hsv)


def color_range_to_transparent(image, min_hsv, max_hsv):
    """Returns image where HSV color range is converted to transparent.

    image: OpenCV format image
    min: Minimum HSV value as np.array
    max: Maximum HSV value as np.array
    """
    bw_image = find_color(image, min_hsv, max_hsv)

    if DEBUG:
        cv2.imwrite('debug.jpg', bw_image)

    # Find the matching pixels
    non_zero_pixels = cv2.findNonZero(bw_image)

    # Add alpha channel to new image
    new_image = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2BGRA)

    for pixel in non_zero_pixels:
        x, y = pixel[0][1], pixel[0][0]
        new_image[x][y] = np.array([0, 0, 0, 0], np.uint8)

    cv2.imwrite('new.png', new_image)


def main():
    file_name = sys.argv[1]
    image = cv2.imread(file_name)
    new_image = color_range_to_transparent(image, GREEN_RANGE_MIN,
                                           GREEN_RANGE_MAX)



if __name__ == '__main__':
    main()
