#!/usr/bin/env python
# encoding: utf-8
"""
Resolve bibitem text to an ADS bibcode.

TOTALLY HACKING

e.g.
0912.5387
http://arxiv.org/abs/0912.5387
"""


def extract_bibitem_bibkey(bibitem):
    """Parse the bibkey in a bibkey"""
    counter = -1
    outer_counter = 0
    bibkey = ""
    for i, c in enumerate(bibitem):
        if c == u'{':
            counter += 1
            if counter == 0:
                outer_counter += 1
        elif c == u'}':
            counter -= 1
        print i, c, counter, outer_counter

        if outer_counter == 2:
            bibkey += c
    bibkey = bibkey.strip('{}')
    return bibkey


def resolve_bibitem(bibitem, referenced_pubs):
    """Returns the publication object for the first referenced publication
    whose bibliographic data matches to text in the bibitem.

    Parameters
    ----------
    bibitem : unicode
        The bibitem string (e.g., \bibitem text)
    referenced_pubs : object
        List of publications referenced by the base document.
    """
    for pub in referenced_pubs:
        for author in pub.authors:
            # author last names need to be in bibtem
            if author[0] not in bibitem:
                continue
            return pub
            # TODO add year matching, etc.


def main():
    from starlit.bib.adsdb import ADSBibDB
    from starlit.bib.adscache import ADSCacheDB
    cachedb = ADSCacheDB(host='localhost', port=27017, ads_db=ADSBibDB())
    adsdb = ADSBibDB(cache=cachedb)
    # adsdb = ADSBibDB()
    # base_pub = adsdb['2007ApJ...667L..49D']
    # print(base_pub.reference_bibcodes)
    bibitem = "\bibitem[{{Fall} \& {Efstathiou}(1980)}]{FalEfs80}{Fall}, S.~M. \& {Efstathiou}, G. 1980, \mnras, 193, 189"
    # ref_pub = resolve_bibitem(bibitem, base_pub.references)
    print("bibkey", extract_bibitem_bibkey(bibitem))
    # print("Matched", ref_pub.bibcode, ref_pub.authors)


if __name__ == '__main__':
    main()
