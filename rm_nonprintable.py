# ------------------------------------------------------
# Warning: Script modifies the existing file! Backup the
#          original file just in case!
#-------------------------------------------------------

# This was written because sometimes my code editor inserts
# invisible control characters which mess up my code compiling.

"""
Removes unprintable characters from a text file(ASCII).
Usage: ./rm_nonprintable.py file_name
"""

import sys
import string


def filter_unprintable(s):
    return ''.join(x for x in s if x in string.printable)


def main():
    arg_count = len(sys.argv)
    if arg_count != 2:
        print(__doc__.strip())
        sys.exit(1)

    if sys.argv[1] in ['--help', '-h']:
        print(__doc__.strip())
        sys.exit(0)

    file_name = sys.argv[1]
    try:
        input_text = open(file_name).read()
    except IOError, e:
        print('Unable to read file.\n%s' % str(e))
        sys.exit(2)

    try:
        f = open(file_name, 'w')
    except IOError, e:
        print('Unable to write to file.\n%s' % str(e))
        sys.exit(2)

    output_text = filter_unprintable(input_text)
    f.write(output_text)
    f.close()


if __name__ == '__main__':
    main()

