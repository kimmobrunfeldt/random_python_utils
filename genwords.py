#!/usr/bin/python

"""
Generates random words and writes them to a file.
Usage ./genwords.py [wordcount]

Default wordcount is ten thousand(10^4).
"""

import random
import string
import sys


charset = string.ascii_lowercase
default_word_count = 10 ** 4
word_min_length = 1
word_max_length = 10
word_separator = ' '
filename = 'words.txt'


def combinations(charsetlen, minlen, maxlen):
    """Returns the amount of different possible combinations with a certain
    character set and password length.
    E.g. charsetlen=26, minlen=1, maxlen=3: 26**1 + 26**2 + 26**3
    """
    lengths = [x for x in range(minlen, maxlen + 1)]
    return sum([charsetlen ** (x + 1) for x in lengths])


def random_word(length):
    return ''.join(random.choice(charset) for x in range(length))


def main():
    if len(sys.argv) > 1 and sys.argv[1].lower() in ['-h', '--help']:
        print(__doc__.strip())
        sys.exit(0)

    word_count = default_word_count
    if len(sys.argv) > 1:
        try:
            word_count = int(eval(sys.argv[1]))
        except:
            print(__doc__.strip())
            sys.exit(1)

    c = combinations(len(charset), word_min_length, word_max_length)
    if word_count > c:
        print('With this charset, you can generate only %s words.' % c)
        print('Note that these are generated randomly, so generating all')
        print('combinations with this algorithm is very slow.')
        sys.exit(2)

    if word_count > 10 ** 5:
        print('Each word is randomly generated, so this might take a while..')

    f = open(filename, 'w')

    words = set()
    while len(words) < word_count:
        length = random.randint(word_min_length, word_max_length)
        word = random_word(length)
        words.add(word)

    f.write(word_separator.join(words))
    f.write('\n')
    f.close()


if __name__ == '__main__':
    main()

