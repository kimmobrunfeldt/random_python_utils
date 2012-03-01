#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Author: Kimmo Brunfeldt

"""
Draws a (sorted and) nice table of a 2-dimensional list.
Handles unicode characters correctly.
"""

import operator
import unicodedata

__author__ = "Kimmo Brunfeldt"


class Table(object):
    """Table is basically 2-dimensional list"""
    def __init__(self, table):
        super(Table, self).__init__()
        self.table_ = table

        # Characters used in drawing.
        self.CORNER = '+'
        self.HORIZONTAL = '-'
        self.VERTICAL = '|'

    def draw(self, sort_column=None, reverse=False):
        """Draws a nice table of 2 dimensional list.
        First row of table is headers, following rows are data.
        Not very efficient, self.table_ is copied!"""

        table = self.table_[:]
        if sort_column is not None:
            # table[0] is not included in sorted, they are the headers.
            table = [table[0]] + sorted(table[1:],
                                        key=operator.itemgetter(sort_column),
                                        reverse=reverse)

        # Convert every item to string. Also add space-pads to sides.
        table = [[' ' + self.all_to_unicode_(element) + ' ' for element in row]
                 for row in table]

        if sort_column is not None:
            table[0][sort_column] += '* '  # Mark sorted column with *.

        # Rotate an array 90 degrees
        # 0 1  ->   2 0           <- (these are the lengths of elements)
        # 2 3       3 1
        # then get max([2, 0]) and max([3, 1]) -> widths = [2, 3]
        widths = [max(self.text_width_(item) for item in row)
                  for row in zip(*table[::-1])]

        # +--+--+
        limiter = ' %s' % self.CORNER + \
                  self.CORNER.join([x * self.HORIZONTAL for x in widths]) + \
                  self.CORNER

        print(limiter)
        for index, row in enumerate(table):
            if index == 1:  # After headers, print limiter.
                print(limiter)

            # Every item in row, separated with '|',
            # space-padded to match max widths.

            line = self.VERTICAL
            for max_width, element in zip(widths, row):
                element = self.strip_nonprintable_(element)
                line += element + ' ' * (max_width - self.text_width_(element))
                line += self.VERTICAL

            print(' %s' % line.encode('UTF-8'))

        print(limiter)
        if sort_column is not None:
            watermark = '* sorted by'
            print(' ' * (len(limiter) - len(watermark)) + watermark)

    # Non-public:

    def text_width_(self, text):
        """Counts text's actual width in terminal when
        fixed-width font is used. http://unicode.org/reports/tr11/ is more
        information about W and F chars."""
        return sum(1 + (unicodedata.east_asian_width(c) in "WF") \
                   for c in text)

    def strip_nonprintable_(self, text):
        """Strips non-printable characters. text must be unicode."""

        # Strip ascii codes 0-31 and 127
        non = list(xrange(32)) + [127]
        return u''.join([u'' if ord(char) in non else char for char in text])

    def all_to_unicode_(self, mixed):
        """Tries to converts anything to unicode."""

        # It already is unicode.
        if isinstance(mixed, unicode):
            return mixed

        if not isinstance(mixed, str):
            mixed = str(mixed)

        try:  # First guess: line is utf-8 encoded
            unicodestring = mixed.decode('utf-8')

        except UnicodeDecodeError:  # It was not utf-8 encoded
            try:
                # Second guess: line is iso-8859-1 encoded
                unicodestring = mixed.decode('iso-8859-1')

            except UnicodeDecodeError:  # It was not iso-8859-1 encoded
                raise

        return unicodestring


if __name__ == '__main__':
    data = [
        ['ID', 'Person'],
        [8, 'Pál Erdős'],
        [23, 'Kurt Gödel'],
        [2, 'Évariste Galois'],
        [3, 'Guillaume de l\'Hôpital'],
        [12, '汉语漢汉语漢汉语漢汉语漢汉语漢汉语漢'],
        [0, 'ἔννεπε, μοῦσα, πολύτροπον'],
        [35, 'ὃς μάλα πολλὰ πλάγχθη'],
    ]

    table = Table(data)
    table.draw()
