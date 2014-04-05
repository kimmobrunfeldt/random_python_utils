"""
Converts certain color pixels to another color.

Usage:
    ./color_pixels.py path_to_image "original_rgb" "new_rgba"

Example:
    ./color_pixels.py image.png
"""

from PIL import Image
import os
import sys


def change_pixel_colors(image, rgba_original, rgba_new):
    """From image, change all rbga_original color pixels to rgba_new color.
    Use RGBA colors.
    """
    pixdata = image.load()
    # Slice the alpha away
    rgb_original = rgba_original[:3]

    if len(rgba_new) == 3:
        rgba_new = rgba_new + (0,)

    for y in range(image.size[1]):
        for x in range(image.size[0]):
            print pixdata[x, y]
            if pixdata[x, y][:3] == rgb_original:
                pixdata[x, y] = rgba_new


def main():
    if len(sys.argv) > 1 and sys.argv[1].lower() in ['-h', '--help']:
        print(__doc__.strip())
        sys.exit(0)

    image_path = sys.argv[1]
    print('Opening image..')
    image = Image.open(image_path)
    image = image.convert("RGBA")

    rgba_original = tuple(sys.argv[2])
    rgba_new = tuple(sys.argv[2])

    print('Changing pixel colors..')
    change_pixel_colors(image, rgba_original, rgba_new)

    file_body, extension = os.path.split(image_path)
    new_imagepath = file_body + '_new.png'
    image.save(new_imagepath, "PNG")
    print('Saved new image to %s' % new_imagepath)


if __name__ == '__main__':
    main()
