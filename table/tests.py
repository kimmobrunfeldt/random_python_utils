#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# My first touch in testing for Python.

"""
Tests for Table class.
"""

import unittest
import table


class TestTable(unittest.TestCase):
    """2 is added to each column's width because elements are
    padded with spaces. For example if column's the widest element
    was "Person", the column's width would be len(" Person ")
    """
    def setUp(self):
        pass

    def test_header_widest(self):
        data = [
            ['ID', 'Person'],
            [0, 'a'],
        ]
        # "Person" will be -> " Person "
        second_column_width = len('Person') + 2

        t = table.Table(data)
        self.assertEqual(t.column_widths_[1], second_column_width,
                         'incorrect column width when header is the widest')

    def test_asian_characters(self):
        data = [
            ['ID', 'Person'],
            [0, '语漢漢漢'],
        ]
        # Asian characters' widths should be counted as 2.
        second_column_width = 4 * 2 + 2  # " 语漢漢漢 "

        t = table.Table(data)
        self.assertEqual(t.column_widths_[1], second_column_width,
                         'width of asian characters were counted wrong')

    def test_non_printable(self):
        data = [
            ['ID', 'Person'],
            [0, '\3\0\0\0abcdefghi'],
        ]
        # non-printable characters should be removed(\3\0\0\0)
        second_column_width = len('abcdefghi') + 2  # " abcdefghi "

        t = table.Table(data)
        self.assertEqual(t.column_widths_[1], second_column_width,
                         'non-printable characters were not removed')

    def test_unicode_conversion(self):
        data = [
            ['ID', 'Person'],
            [0, 'a'],
        ]
        t = table.Table(data)

        already_unicode = u'ä'
        uni = t.all_to_unicode_(already_unicode)
        self.assertEqual(uni, already_unicode, 'incorrect unicode conversion')

        not_str = 44.0
        uni = t.all_to_unicode_(not_str)
        self.assertEqual(uni, u'44.0', 'incorrect unicode conversion')

        latin1_encoded = u'ä'.encode('iso-8859-1')
        uni = t.all_to_unicode_(latin1_encoded)
        self.assertEqual(uni, u'ä', 'incorrect unicode conversion')


if __name__ == '__main__':
    unittest.main()
