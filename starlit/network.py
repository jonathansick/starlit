#!/usr/bin/env python
# encoding: utf-8
"""
Represent reference networks as a networkx graph.

2014-12-08 - Created by Jonathan Sick
"""

import networkx as nx


def init_manuscript_graph(referenced_pubs, add_citations=True, depth=1):
    """Initialize a reference graph for an in-progress manuscript.

    The manuscript is represented as a node named 'ORIGIN'.

    Parameters
    ----------
    referenced_pubs : object
        Publication instances of articles referenced by the manuscript.
    add_citations : bool
        If `True`, then papers that cite this manuscript will be added as well.
    depth : int
        Number of layers of recursion to for getting papers referenced by
        these directly referenced papers.
    """
    g = nx.DiGraph()

    # Add the Base document node
    g.add_node('ORIGIN', type='pub')

    for pub in referenced_pubs:
        add_pub_node(g, pub)
        create_edge(g, 'BASE', pub.bibcode)

        # Add authors
        add_authors(g, pub)

        # Add papers that this paper references
        pub.add_references_to_graph(g, depth=1)

        # Add publications that cite this paper
        if add_citations:
            pub.add_citations_to_graph(g)

    return g


def add_pub_node(g, pub):
    if pub.bibcode not in g:
        g.add_node(pub.bibcode, title=pub.title, kind='pub')


def create_edge(g, from_id, to_id):
    if not g.has_edge(from_id, to_id):
        g.add_edge(from_id, to_id)


def add_authors(g, pub):
    for author in pub.authors:
        # Just use last name to identify an author for now
        author_id = author[0]
        if author_id not in g:
            g.add_node(author_id, parsed_name=author, kind='author')
        # Connect the publication to its author
        if not g.has_edge(pub.bibcode, author_id):
            g.add_edge(pub.bibcode, author_id)
