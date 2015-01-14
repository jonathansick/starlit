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
    def __init__(self, path, ads_cache=None):
        super(BibTexDB, self).__init__()
        self._filepath = path
        with open(path) as bibtex_file:
            bibtex_str = bibtex_file.read()
        self._db = bibtexparser.loads(bibtex_str)
        self._ads_cache = ads_cache

    def __getitem__(self, bibkey):
        return BibTexPub(self._db.entries_dict[bibkey],
                         ads_cache=self._ads_cache)


class BibTexPub(BasePub):
    """A publication backed by bibtex."""
    def __init__(self, pub_dict, ads_cache=None):
        super(BibTexPub, self).__init__()
        self._data = pub_dict
        # FIXME does it make sense to embed a connection to ADSBibDB in
        # each bibtex publication instance???
        self._ads_db = ADSBibDB(cache=ads_cache)
        self._ads_pub = None
        self._encoder = texutils.TexEncoder()

    def __getitem__(self, key):
        return self._data[key]

    def _get_ads_pub(self):
        """Get the representation for the publication via ADS."""
        if self._ads_pub is None:
            print "Getting ADSPub for", self.bibcode
            self._ads_pub = self._ads_db[self.bibcode]
        return self._ads_pub

    @property
    def authors(self):
        """Parsed list of authors; each author is a ``(Last, First)`` tuple."""
        return texutils.parse_bibtex_authors(self._data['author'])

    @property
    def title(self):
        """Title (unicode)"""
        return self._encoder.decode_latex(self._data['title'])

    @property
    def abstract(self):
        """Abstract text (unicode)."""
        return self._encoder.decode_latex(self._data['abstract'])

    @property
    def bibcode(self):
        """The ADS bibcode for this publication."""
        # Look for a bibcode in the records
        # TODO throw exception if not found
        # TODO make a resolver to check that it is a valid bibcode
        if 'adsurl' in self._data:
            bibcode = self._data['adsurl'].split('/')[-1]
            bibcode = bibcode.replace("%26", "&")
            return bibcode

    @property
    def references(self):
        """Records of papers referenced by this publication."""
        ads_pub = self._get_ads_pub()
        return ads_pub.references

    @property
    def reference_bibcodes(self):
        ads_pub = self._get_ads_pub()
        return ads_pub.reference_bibcodes

    @property
    def citations(self):
        """Records of papers referenced by this publication."""
        ads_pub = self._get_ads_pub()
        return ads_pub.citations

    @property
    def citation_bibcodes(self):
        ads_pub = self._get_ads_pub()
        return ads_pub.citation_bibcodes

    @property
    def doi(self):
        """DOI for paper."""
        if 'doi' in self._data:
            return self._data['doi']
        else:
            # FIXME should I throw an exception instead?
            return None

    @property
    def arxiv_id(self):
        """Arxiv identifier for article."""
        print self._data.keys()
        if 'eprint' in self._data:
            eprint = self._data['eprint']
            eprint = eprint.strip('arXiv:')
            return eprint
