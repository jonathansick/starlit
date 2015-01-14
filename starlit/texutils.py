#!/usr/bin/env python
# encoding: utf-8
"""
Utilities for working LaTeX and unicode markup.
"""

from pkg_resources import resource_stream, resource_exists
import xmltodict


def parse_bibtex_authors(bibtex):
    """Parse a bibtex author field into a list of `(Last, First)` tuples."""
    author_list = [i.strip()
                   for i in bibtex.replace('\n', ' ').split(" and ")]
    return [parse_name(a) for a in author_list]


def parse_name(namestr):
    # namestr = namestr.replace(u"{}", u"")
    parts = namestr.split(u",", 1)
    return (parts[0].strip(u"{}"), u" ".join(parts[1:]).strip())


# TODO convert this to a singleton so it is not repeatedly re-initialized?
class TexEncoder(object):
    """Translate between unicode and latex."""
    def __init__(self):
        super(TexEncoder, self).__init__()
        self._load_dataset()

    def _load_dataset(self):
        # Load XML
        path = "data/unicode.xml"
        assert resource_exists(__name__, path)
        with resource_stream(__name__, path) as fd:
            d = xmltodict.parse(fd.read())

        # Build dictionaries mapping unicode to latex and vice versa
        # TODO there is also a 'mathlatex' character set.
        self._unicode_latex = {}
        self._latex_unicode = {}
        for char in d['charlist']['character']:
            if 'latex' not in char:
                continue
            # This little base-16 magic convert unicode code points
            # to unicode characters
            try:
                u = unichr(int(char['@id'][1:], 16))
            except ValueError:
                continue
            self._unicode_latex[u] = char['latex']
            self._latex_unicode[char['latex']] = u

    def decode_latex(self, txt):
        """Convert LaTeX entities in a block of text to unicode.

        Parameters
        ----------
        txt : unicode
            A block of text potentially containing latex entities.

        Returns
        -------
        txt : unicode
            A block of text with all latex entities hopefully converted to
            unicode.
        """
        # FIXME potentially inefficient?
        for ltx, uc in self._latex_unicode.iteritems():
            txt = txt.replace(ltx, uc)
        return txt

    def encode_latex(self, txt):
        """Convert unicode entities in a block of text to LaTeX commands
        where possible.

        Parameters
        ----------
        txt : unicode
            A block of unicode text.

        Returns
        -------
        txt : unicode
            A block of text with unicode characters replaced with equivalent
            latex commands.
        """
        for uc, ltx in self._unicode_latex.iteritems():
            if ltx == ur'\textbackslash':
                # FIXME Hack
                continue
            txt = txt.replace(uc, ltx)
        return txt
