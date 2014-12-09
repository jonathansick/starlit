#!/usr/bin/env python
# encoding: utf-8
"""
Bibliographic database backed by a bibtex file.
"""

import bibtexparser
from .. import texutils

from .base import BasePub
from .adsdb import ADSBibDB


class BibTexDB(object):
    """Bibliographic Database derived from a bibtex file."""
    def __init__(self, path):
        super(BibTexDB, self).__init__()
        self._filepath = path
        with open(path) as bibtex_file:
            bibtex_str = bibtex_file.read()
        self._db = bibtexparser.loads(bibtex_str)

    def __getitem__(self, bibkey):
        return BibTexPub(self._db.entries_dict[bibkey])


class BibTexPub(BasePub):
    """A publication backed by bibtex."""
    def __init__(self, pub_dict):
        super(BibTexPub, self).__init__()
        self._data = pub_dict
        # FIXME does it make sense to embed a connection to ADSBibDB in
        # each bibtex publication instance???
        self._ads_db = ADSBibDB()
        self._ads_pub = None

    def __getitem__(self, key):
        return self._data[key]

    def _get_ads_pub(self):
        """Get the representation for the publication via ADS."""
        if self._ads_pub is None:
            self._ads_pub = self._ads_db[self.bibcode]
        return self._ads_pub

    @property
    def authors(self):
        """Parsed list of authors; each author is a ``(Last, First)`` tuple."""
        return texutils.parse_bibtex_authors(self._data['author'])

    @property
    def title(self):
        """Title (unicode)"""
        return texutils.convert_to_unicode(self._data['title'])

    @property
    def abstract(self):
        """Abstract text (unicode)."""
        return texutils.convert_to_unicode(self._data['abstract'])

    @property
    def bibcode(self):
        """The ADS bibcode for this publication."""
        # Look for a bibcode in the records
        # TODO throw exception if not found
        # TODO make a resolver to check that it is a valid bibcode
        if 'adsurl' in self._data:
            return self._data['adsurl'].split('/')[-1]

    @property
    def references(self):
        """Records of papers referenced by this publication."""
        ads_pub = self._get_ads_pub()
        return ads_pub.references

    @property
    def citations(self):
        """Records of papers referenced by this publication."""
        ads_pub = self._get_ads_pub()
        return ads_pub.citations
