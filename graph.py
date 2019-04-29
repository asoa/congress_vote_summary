#!/usr/bin/env python

from py2neo import Graph, Node, Relationship
import traceback


class Neo4j:
    def __init__(self, **kwargs):
        self.kwargs = {k: v for k,v in kwargs.items()}
        self.graph = Graph(self.kwargs.get("neo4j_url", "bolt:localhost:7687"), auth=('neo4j', ''))
        self.data_object = self.kwargs.get('data_object')

        # method calls
        if self.kwargs.get('graph_init'):
            self.db_config()

    def db_config(self):
        """ create data model indices and constraints (i.e. unique indices) """
        print("***** Create database constraints *****")
        self.graph.run('MATCH (n) DETACH DELETE(n)')  # delete all objects from the
        self.graph.run('CREATE CONSTRAINT ON (s:Senator) ASSERT s.id IS UNIQUE')
        self.graph.run('CREATE CONSTRAINT ON (b:Bill) ASSERT b.roll_call IS UNIQUE')
        self.graph.run('CREATE CONSTRAINT ON (t:Tweet) ASSERT t.id IS UNIQUE')
        self.create_senators(self.data_object.senators)
        self.create_bills(self.data_object.bills)
        self.create_relations(self.data_object.bill_vote_results)

    def query(self, cypher_query):
        try:
            return self.graph.run(cypher_query).to_table()
        except Exception as e:
            if self.kwargs.get('debug'):
                print(traceback.format_exc())

    def create_senators(self, senators):
        """ create senator graph objects in neo4j """
        print("***** creating senator nodes *****")
        [self.graph.create(Node('Senator', senator['party'], id=senator['id'], first_name=senator['first_name'], last_name=senator['last_name'],
                                gender=senator['gender'], party=senator['party'], twitter_account=senator['twitter_account'],
                                state=senator['state'])) for senator in senators]

    def create_bills(self, bills):
        """ create bill graph objects in neo4j """
        print("***** creating bill nodes *****")
        [self.graph.create(Node('Bill', bill['result'], name=bill['id'], roll_call=bill['roll_call'], title=bill['title'],
                                date=bill['date'], d_yes=bill['d_yes'], d_no=bill['d_no'], r_yes=bill['r_yes'],
                                r_no=bill['r_no'], i_yes=bill['i_yes'], i_no=bill['i_no'])) for bill in bills]

    def create_relations(self, relation):
        """ create graph relationship of (senator)-[:votes]->(bill) """
        print("***** creating relationships *****")
        for rel in relation:
            roll_call = rel['roll_call']
            yes_votes = rel['yes']
            no_votes = rel['no']
            for vote in yes_votes:
                cmd = "MATCH (b:Bill {roll_call:{roll_call}}), (s:Senator {id:{vote}}) CREATE (s)-[:voted_yes]->(b)"
                self.graph.run(cmd, roll_call=roll_call, vote=vote)
            for vote in no_votes:
                cmd = "MATCH (b:Bill {roll_call:{roll_call}}), (s:Senator {id:{vote}}) CREATE (s)-[:voted_no]->(b)"
                self.graph.run(cmd, roll_call=roll_call, vote=vote)

def main():
    n = Neo4j()
    # results = n.query('match(hr11:Bill) return hr11.yes_votes')
    # print(results)

if __name__ == "__main__":
    main()
