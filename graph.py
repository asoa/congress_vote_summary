#!/usr/bin/env python

from py2neo import Graph, Node, Relationship
import traceback

#TODO
"""

build a neo4j application hosted on the heroku website that gives the user the ability to search for bills and see
the graph of votes

# https://github.com/neo4j-examples/movies-python-bolt/blob/master/movies.py
# https://neo4j.com/developer/example-project/#_github

"""

class Neo4j:
    def __init__(self, **kwargs):
        self.kwargs = {k: v for k,v in kwargs.items()}
        self.graph = Graph(self.kwargs.get("neo4j_url", "bolt:localhost:7687"), auth=('neo4j', ''))

        # method calls
        self.db_config()

    def db_config(self):
        """ create data model indices and constraints (i.e. unique indices) """
        print("***** Create database constraints ")
        self.graph.run('CREATE CONSTRAINT ON (s:Senator) ASSERT s.id IS UNIQUE')
        self.graph.run('CREATE CONSTRAINT ON (b:Bill) ASSERT b.roll_call IS UNIQUE')
        self.graph.run('CREATE CONSTRAINT ON (t:Tweet) ASSERT t.id IS UNIQUE')

    def query(self, cypher_query):
        try:
            return self.graph.run(cypher_query).to_table()
        except Exception as e:
            if self.kwargs.get('debug'):
                print(traceback.format_exc())

    def create_senators(self, senators):
        """ {"id": "A000360", "first_name": "Lamar", "last_name": "Alexander", "gender": "M", "party": "R", "twitter_account": "SenAlexander", "state": "TN"} """
        print("***** creating senator nodes *****")
        [self.graph.create(Node('Senator', senator['party'], id=senator['id'], name=senator['first_name'] + ' ' + senator['last_name'],
                                gender=senator['gender'], party=senator['party'], twitter_account=senator['twitter_account'],
                                state=senator['state'])) for senator in senators]

    def create_bills(self, bills):
        """ {"id": "hr1644-116", "chamber": "House", "roll_call": 167, "title": "To restore the open internet order of the Federal Communications Commission.", "date": "2019-04-10", "result": "Passed", "d_yes": 231, "d_no": 0, "r_yes": 1, "r_no": 190, "i_yes": 0, "i_no": 0}
        """
        print("***** creating bill nodes *****")
        [self.graph.create(Node('Bill', bill['result'], name=bill['id'], roll_cal=bill['roll_call'], title=bill['title'],
                                date=bill['date'], d_yes=bill['d_yes'], d_no=bill['d_no'], r_yes=bill['r_yes'],
                                r_no=bill['r_no'], i_yes=bill['i_yes'], i_no=bill['i_no'])) for bill in bills]

    def sen_bill_relationship(self, relation):
        """ {"roll_call": 167, "yes": ["A000360", "B001261", "B000575", "B001236"... """
        print("***** creating relationships *****")
        for roll_call in relation:
            bill = self.graph


def main():
    n = Neo4j()
    # results = n.query('match(hr11:Bill) return hr11.yes_votes')
    # print(results)

if __name__ == "__main__":
    main()
