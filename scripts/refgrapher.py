#!/usr/bin/env python
# encoding: utf-8
"""
Build the graph of papers referenced by your own manuscript.
"""

__author__ = "Jonathan Sick"
__copyright__ = "Copyright 2014, Jonathan Sick"
__license__ = "GPL"

import argparse

import networkx as nx

import paperweight.document
from starlit.bib import BibTexDB
from starlit.network import init_manuscript_graph


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

    g = init_manuscript_graph(ref_pubs, depth=1)
    print(nx.info(g))


def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument("tex_path")
    return args.parse_args()


if __name__ == '__main__':
    main()
