#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Table class that has a draw method. It draws (sorted and) nice table of
data. Handles unicode characters correctly.
"""

import operator
import unicodedata

__author__ = "Kimmo Brunfeldt"


class Table(object):
    """This class offers ability to nicely print a table which is in format:

    [ ["header1", "header2"],
      [1, "info1"],
      [2, "info2"]
    ]

    Element can be basically anything that can be sorted and converted
    to string.
    """
    # Characters used in drawing.
    CORNER = '+'
    HORIZONTAL = '-'
    VERTICAL = '|'

    def __init__(self, table):
        super(Table, self).__init__()

        self.headers_ = table.pop(0)
        # Now table contains only data, not headers.
        self.table_ = table
        self.column_widths_ = self.get_column_widths_()

    def draw(self):
        """Draws a nice table of 2 dimensional list.
        First row of table is headers, following rows are data.
        Not very efficient, self.table_ is copied!"""
        # +--+--+
        limiter = self.CORNER + \
                  self.CORNER.join([x * self.HORIZONTAL
                                   for x in self.column_widths_]) + self.CORNER

        # Print headers
        print(limiter)
        self.print_row_(self.headers_)
        print(limiter)

        # Print the actual data
        for row in self.table_:
            self.print_row_(row)

        print(limiter)

    def sort_by_column(self, sort_column, reverse=False):
        self.table_.sort(key=operator.itemgetter(sort_column),
                         reverse=reverse)

    # Non-public:

    def print_row_(self, row):
        """Prints row's items separated with self.VERTICAL,
        and space-padded to match max widths.
        """
        line = self.VERTICAL

        for max_width, element in zip(self.column_widths_, row):

            element = self.all_to_unicode_(element)
            element = self.strip_nonprintable_(element)
            element = u' ' + element + u' '

            element_width = self.width_when_printed_(element)
            line += element + ' ' * (max_width - element_width)
            line += self.VERTICAL

        print(line.encode('utf-8'))

    def get_column_widths_(self):
        column_widths = []

        # For each column, find the element that is the widest when printed.
        for i in range(len(self.headers_)):
            column_width = max(self.width_when_printed_(row[i])
                               for row in self.table_)

            # Check if header is the widest.
            header_width = self.width_when_printed_(self.headers_[i])
            if column_width < header_width:
                column_width = header_width

            # When printed elements are padded with spaces on sides.
            extra_width = 2

            column_width += extra_width
            column_widths.append(column_width)

        return column_widths

    def width_when_printed_(self, mixed):
        """Counts text's actual width in terminal when
        fixed-width font is used. http://unicode.org/reports/tr11/ is more
        information about W and F chars."""
        text = self.all_to_unicode_(mixed)
        text = self.strip_nonprintable_(text)
        return sum(1 + (unicodedata.east_asian_width(c) in "WF") \
                   for c in text)

    def strip_nonprintable_(self, text):
        """Strips non-printable characters. text must be unicode."""

        # Strip ascii codes 0-31 and 127
        non = list(xrange(32)) + [127]
        return u''.join([u'' if ord(char) in non else char for char in text])

    def all_to_unicode_(self, mixed):
        """Tries to converts anything to unicode."""

        if isinstance(mixed, unicode):
            return mixed

        if not isinstance(mixed, str):
            mixed = str(mixed)

        try:
            unicodestring = mixed.decode('utf-8')

        except UnicodeDecodeError:
            try:
                unicodestring = mixed.decode('iso-8859-1')

            # Force decoding with utf-8
            except UnicodeDecodeError:
                unicodestring = mixed.decode('utf-8', 'replace')

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
    table.sort_by_column(0)
    table.draw()
