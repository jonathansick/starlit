#!/usr/bin/env python
# encoding: utf-8
"""
Cache ADS paper requests in MongoDB.

2014-12-09 - Created by Jonathan Sick
"""

from pymongo import MongoClient
from .base import BasePub


class ADSCacheDB(object):
    """Cache of publications built from requests to ADSBibDB.

    The cache is built around MongoDB.
    """
    def __init__(self, host='localhost', port=27017, ads_db=None):
        super(ADSCacheDB, self).__init__()
        client = MongoClient(host, port)
        db = client['starlit']
        self._c = db['cache']  # MongoDB collection
        self._ads_db = ads_db

    def __contains__(self, bibcode):
        if self._c.find({"_id": bibcode}).count() > 0:
            return True
        else:
            return False

    def __getitem__(self, bibcode):
        doc = self._c.find_one({"_id": bibcode})
        return CachePub(doc, ads_db=self._ads_db)

    def insert(self, ads_pub):
        """Insert the ADSPub into the ADSCacheDB."""
        # Form a document dictionary and insert into the DB
        doc = {"_id": ads_pub.bibcode,
               "authors": ads_pub.authors,
               "title": ads_pub.title,
               "abstract": ads_pub.abstract,
               "arxiv_id": ads_pub.arxiv_id,
               "reference_bibcodes": ads_pub.reference_bibcodes,
               "citation_bibcodes": ads_pub.citation_bibcodes}
        self._c.save(doc)


class CachePub(BasePub):
    """A publication cached by ADSCacheDB (MongoDB).

    Parameters
    ----------
    doc : object
        PyMongo document instance.
    """
    def __init__(self, doc, ads_db=None):
        super(CachePub, self).__init__()
        self._doc = doc
        self._ads_db = ads_db

    @property
    def authors(self):
        """Parsed list of authors; each author is a ``(Last, First)`` tuple."""
        return self._doc['authors']

    @property
    def title(self):
        """Title (unicode)"""
        return self._doc['title']

    @property
    def abstract(self):
        """Abstract text (unicode)."""
        return self._doc['abstract']

    @property
    def bibcode(self):
        """The ADS bibcode for this publication."""
        return self._doc['_id']

    @property
    def references(self):
        """Records of papers referenced by this publication."""
        bibcodes = self._doc['reference_bibcodes']
        # FIXME might want rectify what should actually be returned
        if self._ads_db is not None:
            pubs = [self._ads_db[bibcode] for bibcode in bibcodes]
            return pubs
        else:
            return bibcodes

    @property
    def citations(self):
        """Records of papers referenced by this publication."""
        bibcodes = self._doc['citation_bibcodes']
        # FIXME might want to recify what should be returned if no ADS DB
        if self._ads_db is not None:
            pubs = [self._ads_db[bibcode] for bibcode in bibcodes]
            return pubs
        else:
            return bibcodes

    @property
    def doi(self):
        """DOI for paper."""
        if 'doi' in self._doc:
            return self._doc['doi']
        else:
            # FIXME should I throw an exception instead?
            return None

    @property
    def arxiv_id(self):
        """Arxiv identifier for article."""
        print self._data.keys()
        if 'arxiv_id' in self._doc:
            return self._doc['arxiv_id']
