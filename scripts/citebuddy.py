#!/usr/bin/env python
# encoding: utf-8
"""
Suggest citations based on the references you've already made!
"""

__author__ = "Jonathan Sick"
__copyright__ = "Copyright 2014, Jonathan Sick"
__license__ = "GPL"

import argparse

import networkx as nx

import paperweight.document
from starlit.bib import BibTexDB


def main():
    args = parse_args()

    doc = paperweight.document.FilesystemTexDocument(args.tex_path)
    bib_keys = doc.bib_keys
    bibdb = BibTexDB(doc.bib_path)
    ref_pubs = []
    for bib_key in bib_keys:
        pub = bibdb[bib_key]
        ref_pubs.append(pub)
        print(pub.bibcode)
        print(pub.title)
        print([a[0] for a in pub.authors])

    g = build_network(ref_pubs)
    print(nx.info(g))


def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument("tex_path")
    return args.parse_args()


def build_network(referenced_pubs):
    """Build a network around this paper from a list of bibcodes."""
    g = nx.DiGraph()

    # Add the Base document node
    g.add_node('ORIGIN', type='pub')

    for pub in referenced_pubs:
        if pub.bibcode not in g:
            print pub.bibcode
            g.add_node(pub.bibcode, title=pub.title, kind='pub')
            # Connect referring pub to this paper
            g.add_edge('BASE', pub.bibcode)
            # Add authors
            for author in pub.authors:
                # Just use last name to identify an author for now
                author_id = author[0]
                if author_id not in g:
                    g.add_node(author_id, parsed_name=author, kind='author')
                # Connect the publication to its author
                g.add_edge(pub.bibcode, author_id)

    return g


if __name__ == '__main__':
    main()
