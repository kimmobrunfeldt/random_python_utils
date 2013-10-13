"""
Removes greenscreen from an image.
Usage: python greenscreen_remove.py image.jpg
"""

from PIL import Image
import sys
import os


GREEN_THRESHOLD = 100


def main():
    # Load image and convert it to RGBA, so it contains alpha channel
    file_path = sys.argv[1]
    name, ext = os.path.splitext(file_path)
    im = Image.open(file_path)
    im = im.convert('RGBA')

    # Go through all pixels and turn each 'green' pixel to transparent
    pix = im.load()
    width, height = im.size
    for x in range(width):
        for y in range(height):
            r, g, b, a = pix[x, y]
            if g > r + b and g >= GREEN_THRESHOLD:
                pix[x, y] = (0, 0, 0, 0)

    im.save(name + '.png')


if __name__ == '__main__':
    main()
