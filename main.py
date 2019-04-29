#!/usr/bin/env python

from propublica import ProPublica
from graph import Neo4j


def main():
    data = ProPublica(mongo_init=False, data_init=False)
    graph = Neo4j(graph_init=False, data_object=data)

    # create tweet nodes #TODO


if __name__ == "__main__":
    main()
