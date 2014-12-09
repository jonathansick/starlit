#!/usr/bin/env python
# encoding: utf-8
"""
Some badly coded utilities for converting latex/bibtex marked up text into
unicode.
"""

import itertools

from bibtexparser.latexenc import unicode_to_latex, \
    unicode_to_crappy_latex1, \
    unicode_to_crappy_latex2


def parse_bibtex_authors(bibtex):
    """Parse a bibtex author field into a list of `(Last, First)` tuples."""
    author_list = [i.strip()
                   for i in bibtex.replace('\n', ' ').split(" and ")]
    return [parse_name(a) for a in author_list]


def parse_name(namestring):
    """Make people names as tuples of (surname, firstnames)
    or surname, initials.

    Adapted from bibtexparser
    """
    if ',' in namestring:
        namesplit = namestring.split(',', 1)
        last = namesplit[0].strip()
        firsts = [i.strip() for i in namesplit[1].split()]
    else:
        namesplit = namestring.split()
        last = namesplit.pop()
        firsts = [i.replace('.', '. ').strip() for i in namesplit]
    if last in ['jnr', 'jr', 'junior']:
        last = firsts.pop()
    for item in firsts:
        if item in ['ben', 'van', 'der', 'de', 'la', 'le']:
            last = firsts.pop() + ' ' + last
    last = last.strip(u"{}")  # FIXME seems like bibtexparser should do this
    parsed_name = (last, ' '.join(firsts))
    return parsed_name


def convert_to_unicode(latex_str):
    """
    Convert accent from latex to unicode style.

    Adapted from bibtexparser.
    """
    if '\\' in latex_str or '{' in latex_str:
        for k, v in itertools.chain(unicode_to_crappy_latex1,
                                    unicode_to_latex):
            if v in latex_str:
                latex_str = latex_str.replace(v, k)

        # If there is still very crappy items
        if '\\' in latex_str:
            for k, v in unicode_to_crappy_latex2:
                if v in latex_str:
                    parts = latex_str.split(str(v))
                    for key, latex_str in enumerate(parts):
                        if key+1 < len(parts) and len(parts[key+1]) > 0:
                            # Change order to display accents
                            parts[key] = parts[key] + parts[key+1][0]
                            parts[key+1] = parts[key+1][1:]
                    latex_str = k.join(parts)
    return latex_str
