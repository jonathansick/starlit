#!/usr/bin/env python
# encoding: utf-8
"""
Suggest citations based on the references you've already made!
"""

__author__ = "Jonathan Sick"
__copyright__ = "Copyright 2014, Jonathan Sick"
__license__ = "GPL"

import argparse

import paperweight.document
from starlit.bib import BibTexDB


def main():
    args = parse_args()

    doc = paperweight.document.FilesystemTexDocument(args.tex_path)
    bib_keys = doc.bib_keys
    bibdb = BibTexDB(doc.bib_path)
    for bib_key in bib_keys:
        print(bibdb[bib_key].authors)


def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument("tex_path")
    return args.parse_args()


if __name__ == '__main__':
    main()
