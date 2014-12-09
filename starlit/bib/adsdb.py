#!/usr/bin/env python
# encoding: utf-8
"""
Bibliographic database backed by the ADS API.

The intention is to have classes that the API of BibTexDB and BibTexPub.

.. todo:: Add a caching mechanism; maybe with MongoDB?

2014-12-07 - Created by Jonathan Sick
"""

import ads

# import texutils


class ADSBibDB(object):
    """Bibliographic database derived from the NASA/SAO ADS API."""
    def __init__(self):
        super(ADSBibDB, self).__init__()

    def __getitem__(self, bibcode):
        """Access a paper given its bibcode."""
        # TODO add caching here
        # FIXME is there a better api for getting a single publication?
        ads_query = ads.query(query=bibcode)
        return ADSPub(ads_query.next())


class ADSPub(object):
    """A publication record obtained from the NASA/SAO ADS API.

    Parameters
    ----------
    ads_article : :class:`ads.Article`
        The article instance obtained from ``ads``.
    """
    def __init__(self, ads_article):
        super(ADSPub, self).__init__()
        self._article = ads_article

    @property
    def authors(self):
        """Parsed list of authors; each author is a ``(Last, First)`` tuple."""
        authors = []
        for a in authors:
            a_last, a_first = a.split(',')
            authors.append((a_last.strip(), a_first.strip()))
        return authors

    @property
    def title(self):
        """Title (unicode)"""
        # why does ads give the title as a list?
        return self._article['title'][0]

    @property
    def abstract(self):
        """Abstract text (unicode)."""
        return self._article.abstract

    @property
    def bibcode(self):
        """The ADS bibcode for this publication."""
        return self._article.bibcode

    @property
    def references(self):
        """Publications referenced by this publication."""
        # TODO could check a MongoDB cache here
        return [ADSPub(ref) for ref in self._article.references]

    @property
    def citations(self):
        """Publications that cite this publication."""
        # TODO could check a MongoDB cache here
        return [ADSPub(ref) for ref in self._article.citations]
