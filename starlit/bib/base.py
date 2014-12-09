#!/usr/bin/env python
# encoding: utf-8
"""
Base classes for papers.

2014-12-09 - Created by Jonathan Sick
"""


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
            Depth of recursion (currently not implemented).
        """
        # FIXME Refactor the creation of nodes from publications
        # Also refactor adding authors to graph
        for pub in self.references:
            g.add_node(pub.bibcode, title=pub.title, kind='pub')
            # Connect referring pub to this paper
            g.add_edge(self.bibcode, pub.bibcode)
            # Add authors of the referenced paper.
            for author in pub.authors:
                # Just use last name to identify an author for now
                author_id = author[0]
                if author_id not in g:
                    g.add_node(author_id, parsed_name=author, kind='author')
                # Connect the publication to its author
                g.add_edge(pub.bibcode, author_id)

    def add_citations_to_graph(self, g):
        """Add all citations to this paper to the graph `g`.

        Parameters
        ----------
        g : :class:`networkx.DiGraph`
            A graph instance.
        """
        # FIXME Refactor the creation of nodes from publications
        # Also refactor adding authors to graph
        for pub in self.citations:
            g.add_node(pub.bibcode, title=pub.title, kind='pub')
            # Connect referring pub to this paper
            # NOTE reversed since edge is *to* self.
            g.add_edge(pub.bibcode, self.bibcode)
            # Add authors of the citing paper
            for author in pub.authors:
                # Just use last name to identify an author for now
                author_id = author[0]
                if author_id not in g:
                    g.add_node(author_id, parsed_name=author, kind='author')
                # Connect the publication to its author
                g.add_edge(pub.bibcode, author_id)
