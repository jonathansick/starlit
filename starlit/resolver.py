#!/usr/bin/env python
# encoding: utf-8
"""
Resolve bibitem text to an ADS bibcode.

TOTALLY HACKING

e.g.
0912.5387
http://arxiv.org/abs/0912.5387


"""
# import re


def parse_bibitem(bibitem):
    # cite_pattern = re.compile(ur'\\cite*{(.*?)}', re.UNICODE)
    # pattern = re.compile(ur'\\cite*{(.*?)}', re.UNICODE)
    first_sep_index = bibitem.index('{')
    final_sep_index = bibitem.index('}')
    bibkey = bibitem[first_sep_index + 1: final_sep_index]
    citation_str = bibitem[final_sep_index + 1:]
    return bibkey, citation_str


def resolve_citation(bibkey, bibitem, referenced_pubs):
    """Resolve a citation string into a BibCode,
    e.g. Berczik, P., Merritt, D., Spurzem, R., \& Bischof, H.-P. 2006,
    \apj, 642, L21
    """
    bibitem = bibitem.replace(" \\&", "")
    words = [w.strip(', ') for w in bibitem.split(' ')]
    for i, w in enumerate(words):
        # find word that is a year
        print i, w
        if w.isdigit() and (len(w) == 4):
            year_index = i
            year = int(w)
    last_names = words[:year_index][::2]
    print(year)
    print(last_names)
    for pub in referenced_pubs:
        for n_bibitem, n_ref in zip(last_names, pub.authors):
            # Make sure last names match
            # FIXME worried about unicode variants here
            if n_bibitem != n_ref[0]:
                continue
            # Make sure year matches
            if year != pub.year:
                continue
            # Otherwise we've found a match:
            return pub


def main():
    from starlit.bib.adsdb import ADSBibDB
    from starlit.bib.adscache import ADSCacheDB
    cachedb = ADSCacheDB(host='localhost', port=27017, ads_db=ADSBibDB())
    adsdb = ADSBibDB(cache=cachedb)
    bibitem = "\bibitem[Berczik et al.(2006)]{BMSB06}Berczik, P., Merritt, D., Spurzem, R., \& Bischof, H.-P. 2006, \apj, 642, L21"
    bibkey, citation_str = parse_bibitem(bibitem)
    resolve_citation(bibkey, citation_str, None)


if __name__ == '__main__':
    main()
