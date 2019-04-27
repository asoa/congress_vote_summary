#!/usr/bin/env python

from propublica import ProPublica
from graph import Neo4j

def main():
    p = ProPublica(mongo_init=False, data_init=True)
    graph = Neo4j()

    # create senator and bill nodes
    # graph.create_senators(p.senators)
    # graph.create_bills(p.bills)

    # create tweet nodes #TODO
    # graph.create_bill(p.bills)
    # p.get_senators()
    # p.get_recent_votes()
    # p.get_roll_call()

    # results = p.bill_vote_results
    # for d in results:
    #     for k,v in d.items():
    #         print(f'\n***** Voting results for roll_call vote: {k} ***** \n')
    #         print('Yes votes: {}'.format(v['yes']))
    #         print('No votes: {}'.format(v['no']))

if __name__ == "__main__":
    main()
