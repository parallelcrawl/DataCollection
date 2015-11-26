#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import unicodedata
from util import encoding

""" Utility functions to reliably read text with
    unknown of broken encoding and return proper
    unicode.
"""


class TextSanitizer():

    @staticmethod
    def clean_whitespace(s):
        """ Cleans empty lines and repeated whitespace """
        # remove empty lines
        s = [l.strip() for l in s.split("\n") if l.strip()]
        return "\n".join(re.sub("\s+", " ", l) for l in s)

    @staticmethod
    def _sanitize(c):
        """ Returns space if character is not printable """
        category = unicodedata.category(c)[0]
        if category == 'C':  # remove control characters
            return ' '
        if category == 'Z':  # replace all spaces by normal ones
            return ' '
        return c

    @staticmethod
    def clean_utf8(s):
        """ Removes most funny characters from Unicode """
        if not isinstance(s, unicode):
            return s
        s = unicodedata.normalize('NFC', s)
        sanitized_lines = []
        for line in s.split("\n"):
            sanitized_lines.append(u"".join(map(TextSanitizer._sanitize,
                                                line)))
        return "\n".join(sanitized_lines)

    @staticmethod
    def to_unicode(text):
        """ Produce unicode from text of unknown encoding """
        return encoding.to_unicode(text)

    @staticmethod
    def clean_text(text, sanitize=True, clean_whitespace=True):
        """ Input: unicode string, output: sanitized & cleaned string """
        if sanitize:
            text = TextSanitizer.clean_utf8(text)
        if clean_whitespace:
            text = TextSanitizer.clean_whitespace(text)
        return text

    @staticmethod
    def read_text(filehandle, sanitize=True, clean_whitespace=True):
        """ Read from filehandle and use best-effort decoding/cleaning """
        text = filehandle.read()
        if not text:
            return u''
        text = TextSanitizer.to_unicode(text)
        return TextSanitizer.clean_text(text, sanitize, clean_whitespace)

    @staticmethod
    def read_file(filename, sanitize=True, clean_whitespace=True):
        """ Read a file and use best-effort decoding/cleaning """
        try:
            f = open(filename, 'r')
            return TextSanitizer.read_text(f, sanitize, clean_whitespace)
        except IOError:
            sys.stderr.write("Cannot read file: %s\n" % filename)
            return ""
