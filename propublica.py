#!/usr/bin/env python

import requests
import json
from collections import defaultdict
from mongo_db import MongoDb
from util import secrets_BU  # change this to secrets for your api
from graph import Neo4j
from util.helpers import write_json, load_json
import os


class ProPublica:
    def __init__(self, **kwargs):
        """
        Attributes:
            senators: (list) of dict objects with senator information
            bills: (list) of dict objects of recent bills
            bill_vote_results (list) of dict objects of the bill voting summary result
            vote_tally: (list) of dict objects of bill votes by senator
        """
        self.kwargs = {k:v for k,v in kwargs.items()}
        self.secrets = secrets_BU.passwords
        self.mongo_init = self.kwargs.get('mongo_init', False)
        self.mongo_client = MongoDb(do_init=self.mongo_init)
        self.senators = []
        self.bills = []
        self.bill_vote_results = []
        self.vote_tally = []
        self.headers = {'X-API-Key': self.secrets['propublica']}

        # method calls
        if self.kwargs.get('data_init'):
            self.get_senators()
            self.get_recent_bills()
            self.get_roll_call()
            self.save_data()
        else:
            self.senators, self.bills, self.bill_vote_results, _ = load_json()

    def get_senators(self):
        """ get senator information """
        url = 'https://api.propublica.org/congress/v1/115/senate/members.json'
        response = requests.get(url, headers=self.headers).text  # returns str
        senators = json.loads(response)['results'][0].get('members')

        for senator in senators:
            d = {'id': senator['id'], 'first_name': senator['first_name'], 'last_name': senator['last_name'],
                 'gender': senator['gender'], 'party': senator['party'], 'twitter_account': senator['twitter_account'],
                 'state': senator['state']}
            self.senators.append(d)

        return self.senators
        # [print(senator) for senator in self.senators]

    def get_recent_bills(self):
        """ connect to votes endpoint to get the most recent votes """

        url = 'https://api.propublica.org/congress/v1/both/votes/recent.json'
        response = requests.get(url, headers=self.headers).text  # returns str
        bills = json.loads(response)['results']['votes']  # create json object from str

        for vote in bills:
            if 'bill_id' in vote['bill']:  # checks for bill_id, indicating that the vote is for a bill
                # creates a dictionary with key(bill_id)
                d = {'id': vote['bill']['bill_id'], 'chamber': vote['chamber'], 'roll_call': vote['roll_call'],
                        'title': vote['bill']['title'], 'date': vote['date'], 'result': vote['result'],
                        'd_yes': vote['democratic']['yes'], 'd_no': vote['democratic']['no'],
                        'r_yes': vote['republican']['yes'], 'r_no': vote['republican']['no'],
                        'i_yes': vote['independent']['yes'], 'i_no': vote['independent']['no']}

                self.bills.append(d)
            else:  # vote was not a bill (i.e. 'nomination')
                continue
        return self.bills
        # self.write_db('bills')

        # [print(vote) for vote in votes]

    def get_roll_call(self):
        """ connect to vote endpoint to get roll call votes for all recent bills
        GET https://api.propublica.org/congress/v1/{congress}/{chamber}/sessions/1/votes/{roll-call-number}.json
        """
        self.vote_tally = []  # list of default dict objects
        for vote in self.bills:  # iterate over vote dictionaries
            # for k,v in vote.items():
            roll_call_results = defaultdict(list)  # instantiates a dictionary with a value of an empty list
            # roll_call_id = v[1]
            roll_call_id = vote['roll_call']
            url = f'https://api.propublica.org/congress/v1/115/senate/sessions/1/votes/{roll_call_id}.json'
            headers = {'X-API-Key': self.secrets['propublica']}
            response = requests.get(url, headers=headers).text

            representatives = json.loads(response)['results']['votes']['vote']['positions']
            for rep in representatives:  # iterates over each congressman and appends their info and vote to the default list
                d = {'member_id': rep['member_id'], 'name': rep['name'], 'party': rep['party'],
                     'state': rep['state'], 'vote': rep['vote_position']}
                roll_call_results[roll_call_id].append(d)
                # roll_call_results[roll_call_id].append([rep['member_id'],rep['name'],rep['party'],rep['state'],rep['vote_position']])
            self.vote_tally.append(roll_call_results)  # appends the dictionary with voting information to vote_tally

        for bill in self.vote_tally:  # iterate over each vote result
            roll_call_id = list(bill.keys())[0]
            #  loop over each roll and its list of voting results by member of congress -- filter the yes votes
            for k,v in bill.items():
                bill_yes = [rep['member_id'] for rep in v if rep['vote'] == 'Yes']
                bill_no = [rep['member_id'] for rep in v if rep['vote'] == 'No']
            # bill_yes = [rep[1] for roll_call,lists in bill.items() for rep in lists if rep[4] == 'Yes']
            #  loop over each roll and its list of voting results by member of congress -- filter the no votes
            # bill_no = [rep[1] for roll_call, lists in bill.items() for rep in lists if rep[4] == 'No']
            #  dictionary with roll_call_id as key and nested dict values with yes and no as keys
            # self.bill_vote_results[roll_call_id] = {'yes': bill_yes, 'no': bill_no}
                self.bill_vote_results.append({'roll_call': roll_call_id, 'yes': bill_yes, 'no': bill_no})

        return self.bill_vote_results
        # self.write_db('roll_call')

    def neo4j_init(self):
        """ create senator and bill neo4j nodes """
        self.neo4j_driver.create_senators()

    def get_twitter_accounts(self):
        """
        create dataframe of the twitter accounts (from congress-legislatures) for all of congress, then write to mongo db
        schema: [account_collection] person: twitter_handle  [tweet_collection] person: tweet(text_only)

        """

    def bill_summary_stats(self):
        """
        create df with relevant data
        index=bill_name columns=[bill_id, title, latest_action, date, vote_type, roll_call, d_votes, r_votes, result]

        """

        # TODO: create dataframe from records in self.votes created in get_recent_bills()

    def write_db(self, collection_name):
        """ write data to mongo """

        if collection_name == 'bills':
            self.mongo_client.bills.insert_many(self.bills)
        else:
            self.mongo_client.roll_call.insert_many(self.bill_vote_results)

    def save_data(self):
        """ save senators, bills and roll_call """
        write_json(self.bills, bill=True)
        write_json(self.bill_vote_results, roll_call=True)
        write_json(self.senators, senators=True)
        write_json(self.vote_tally, tally=True)


def main():
    p = ProPublica(mongo_init=False, data_init=False)
    results = p.bill_vote_results
    for d in results:
        for k,v in d.items():
            print(f'\n***** Voting results for roll_call vote: {k} ***** \n')
            print('Yes votes: {}'.format(v['yes']))
            print('No votes: {}'.format(v['no']))


if __name__ == "__main__":
    main()
