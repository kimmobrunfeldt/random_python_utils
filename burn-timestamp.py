"""
Install pip with Freetype2 support

    brew install freetype
    pip install Pillow


The script burns images' modification times to images. Images are sorted by
modification time and copied with increasing number as filenames.

Usage:

    python burn-timestamp.py <directory> <pattern>

Where <directory> is the directory where images are located and
      <pattern> is pattern to match images, for example "*.jpg".

Example:

    python burn-timestamp.py DCIM/ "*.JPG"

Burned images are copied to stampimages/ folder.
"""

import glob
import errno
import os
import time
import sys

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


FONT_PATH = "/Library/Fonts/Arial.ttf"

# This value will be added to modification time
TIME_OFFSET_SECONDS = 3600 * 7

STAMP_COLOR = (255, 255, 255)
STAMP_ALPHA = 170
STAMP_FORMAT = "%H:%M"

# Position for timestamp text
# These must be strings, they are evaluated to calculate the final value
X_POSITION = "{width} - 220"
Y_POSITION = "10"

OUTPUT_DIRECTORY = 'stampimages'


def draw_stamp(img, mod_time):
    stamp = time.strftime(STAMP_FORMAT, time.localtime(mod_time + TIME_OFFSET_SECONDS))

    width, height = img.size
    font = ImageFont.truetype(FONT_PATH, 80)

    watermark = Image.new("RGBA", img.size)
    draw = ImageDraw.Draw(watermark)

    position = (eval(X_POSITION.format(width=width).replace(' ', '')),
                eval(Y_POSITION.format(height=height).replace(' ', '')))
    draw.text(position, stamp, fill=STAMP_COLOR, font=font)

    mask = watermark.convert("L").point(lambda x: min(x, STAMP_ALPHA))
    # Apply this mask to the watermark image, using the alpha filter to
    # make it transparent
    watermark.putalpha(mask)

    # Paste the watermark (with alpha layer) onto the original imag
    img.paste(watermark, None, watermark)


def mkdirp(path):
    """mkdir -p functionality
    Creates directory if it doesn't exist.
    Returns True if the directory existed and False if not.
    """
    try:
        os.makedirs(path)
    except OSError, e:
        if e.errno == errno.EEXIST:
            return True
        else:
            raise

    return False


def yes_or_die(message):
    print(message)
    answer = raw_input('Do you want to proceed? (y/n) ')
    if answer.lower() not in ('y', 'yes'):
        sys.exit(3)


def time_left(done, total, start_time):
    """Takes amount of done tasks, total amount of tasks and unix timestamp
    of starting time. Remaining seconds is returned.
    """
    elapsed = time.time() - start_time
    time_per_one = float(done / elapsed)
    remaining = (total - done) * time_per_one
    return remaining


def replace_print(x):
    sys.stdout.write("\r%s" % x)
    sys.stdout.flush()


def main():
    directory = sys.argv[1]
    pattern = sys.argv[2]

    files = glob.glob(os.path.join(directory, pattern))

    paths = []
    for path in files:
        if not os.path.isfile(path):
            print('Skip: %s' % path)
            continue

        mod_time = os.path.getmtime(path)
        paths.append((mod_time, path))

    # Sort by modification time
    paths.sort()

    print('Stamping total of %s images..' % len(paths))
    exists = mkdirp(OUTPUT_DIRECTORY)
    if exists:
        yes_or_die('%s already exists, new images will be copied there.' %
                   OUTPUT_DIRECTORY)
    else:
        print('Created directory %s' % OUTPUT_DIRECTORY)

    start_time = time.time()
    print('')
    for index, (mod_time, path) in enumerate(paths, start=1):

        # Open old image and stamp it with modification time
        img = Image.open(path)
        img.convert('RGBA')
        draw_stamp(img, mod_time)
        new_path = os.path.join(OUTPUT_DIRECTORY, str(index).zfill(10) + '.png')
        img.save(new_path)

        remaining = round(time_left(index, len(paths), start_time), 1)
        replace_print('Remaining:   time %s secs      images left %s' %
            (str(remaining).rjust(10), str(len(paths) - index).rjust(6)))

    print('')


if __name__ == '__main__':
    main()
