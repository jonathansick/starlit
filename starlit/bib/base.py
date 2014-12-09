#!/usr/bin/env python
# encoding: utf-8
"""
Base classes for papers.

2014-12-09 - Created by Jonathan Sick
"""

from ..network import add_pub_node, create_edge, add_authors


class BasePub(object):
    """Base class for all publication representations."""
    def __init__(self):
        super(BasePub, self).__init__()

    def add_references_to_graph(self, g, depth=1):
        """Add all references to this paper to the graph `g`.

        Parameters
        ----------
        g : :class:`networkx.DiGraph`
            A graph instance.
        depth : int
            Depth of recursion.
        """
        for pub in self.references:
            add_pub_node(g, pub)
            # Connect referring pub to this paper
            create_edge(g, self.bibcode, pub.bibcode)
            # Add authors of the referenced paper.
            add_authors(g, pub)
            # Add papers recursively
            if depth > 1:
                pub.add_references_to_graph(g, depth=depth - 1)

    def add_citations_to_graph(self, g):
        """Add all citations to this paper to the graph `g`.

        Parameters
        ----------
        g : :class:`networkx.DiGraph`
            A graph instance.
        """
        for pub in self.citations:
            add_pub_node(g, pub)
            # Connect referring pub to this paper
            # NOTE reversed since edge is *to* self.
            create_edge(g, pub.bibcode, self.bibcode)

            # Add authors of the citing paper
            add_authors(g, pub)
