#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Regular expression to match http and https URLs.
# This is NOT a validator regex. This is a regex that
# primary determines URLs that are pasted in an IRC channel.
# It can also be used to find all URLs in a HTML code or email.

import re


# Match everything that starts with http:// or https://
# and ends to: '"<>  or whitespace

URL_REGEX = r"""https?://[^'"<>\s]+"""

#             ^      ^       ^    ^
#             |      |       |    |
#             |      |       |    |
# Use """ to         |       |    |
# declare string     |       |    |
#                    |       |    |
#    s?   0 or 1 's'         |    |
#         chars to match     |    |
#         http or https      |    |
#                            |    |
#[^'"<>\s]  Match everything      |
#           except these chars    |
#           inside [] brackets.   |
#           If you want new ender |
#           char, put it here.    |
#                                 |
#             +  There must be at
#                least 1 valid char
#                after the http://
#                part.


def printred(s):  # Prints text in red.
    if len(s) > 0:  # Don't do anything if string is empty.
        if s[-1] == '\n':
            s = s[:-1]  # Remove lineterminator if one.
        print('\033[0;31m' + str(s) + '\033[m')


def printbold(s):  # Prints text in bold.
    if len(s) > 0:
        if s[-1] == '\n':
            s = s[:-1]
        print('\033[0;1m' + str(s) + '\033[m')


if __name__ == '__main__':

    test_urls = [
        "http://google.com",
        "https://google.com",
        "http://validurlthatdoesnotexist.com",
        "http://",
        "http://1",
        "http://mysite.com:invalidport1235",
    ]

    test_text = """
    <invalidhtmlstartshere>
    <html>
    <a href="http://www.google.fi">check cool_site</a>
    adsgdsalkgjdsag"http://google.com"asdgdasg
    ____________________http://google.com__underlines_dont_stop_link_!
    ______http://google.com>
    aasdasdasdhttps://sslpoweredsite.com asdasdasd
    https://google.com
    """

    r = re.compile(URL_REGEX)

    printbold('Testing what items(URLs) in the test_list match URL regex.')
    printbold('Urls that did not match the regex are printed in red.\n')

    for url in test_urls:
        m = re.match(r, url)

        if m is not None:
            print(m.group(0))
        else:
            printred(url)

    printbold('\nAll URLs that were found from test_text:')

    for match in re.findall(r, test_text):
        print(match)
