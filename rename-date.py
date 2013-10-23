"""
Renames all files on a directory to their modification date.

Usage:   python rename-date.py directory *pattern*
Example: python rename-date.py gifs "*.gif"
"""

import glob
import os
import time
import shutil
import sys


def main():
    directory = sys.argv[1]
    pattern = sys.argv[2]

    files = glob.glob(os.path.join(directory, pattern))

    print files, pattern
    for path in files:
        if not os.path.isfile(path):
            print path
            continue

        mod_time = os.path.getmtime(path)
        stamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(mod_time))
        _, ext = os.path.splitext(path)
        new_name = stamp + ext

        base, _ = os.path.split(path)
        new_path = os.path.join(base, new_name)

        print('Rename %s -> %s' % (path, new_path))
        shutil.move(path, new_path)



if __name__ == '__main__':
    main()
