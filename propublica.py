#!/usr/bin/env python

import requests
import json
from collections import defaultdict


class ProPublica:
    def __init__(self, **kwargs):
        self.kwargs = {k:v for k,v in kwargs.items()}
        self.api_key = '<replace me>'
        self.bills = None
        self.votes = []
        self.bill_vote_results = {}

    def get_recent_bills(self):
        """ connect to bill endpoint to get 20 most recent bills """

        url = 'https://api.propublica.org/congress/v1/both/votes/recent.json'
        headers = {'X-API-Key': self.api_key}
        response = requests.get(url, headers=headers).text  # returns str
        bills = json.loads(response)['results']['votes']  # create json object from str

        for vote in bills:
            if 'bill_id' in vote['bill']:
                d = {vote['bill']['bill_id']:
                         [vote['chamber'],vote['roll_call'],vote['bill']['title'],vote['date'],vote['result'],
                          vote['democratic']['yes'],vote['democratic']['no'],
                          vote['republican']['yes'],vote['republican']['no'],
                          vote['independent']['yes'],vote['independent']['no']]}
                self.votes.append(d)
            else:  # vote was not a bill (i.e. 'nomination')
                continue

        # [print(vote) for vote in votes]

    def get_roll_call(self):
        """ connect to vote endpoint to get roll call votes for all recent bills
        GET https://api.propublica.org/congress/v1/{congress}/{chamber}/sessions/1/votes/{roll-call-number}.json
        """
        vote_tally = []  # list of default dict objects
        for vote in self.votes:
            for k,v in vote.items():
                d = defaultdict(list)
                roll_call_id = v[1]
                url = f'https://api.propublica.org/congress/v1/115/senate/sessions/1/votes/{roll_call_id}.json'
                headers = {'X-API-Key': self.api_key}
                response = requests.get(url, headers=headers).text

                representatives = json.loads(response)['results']['votes']['vote']['positions']
                for rep in representatives:
                    d[roll_call_id].append([rep['member_id'],rep['name'],rep['party'],rep['state'],rep['vote_position']])
                vote_tally.append(d)

        for bill in vote_tally:
            roll_call_id = list(bill.keys())[0]
            bill_yes = [rep[1] for roll_call,lists in bill.items() for rep in lists if rep[4] == 'Yes']
            bill_no = [rep[1] for roll_call, lists in bill.items() for rep in lists if rep[4] == 'No']
            self.bill_vote_results[roll_call_id] = {'yes': bill_yes, 'no': bill_no}
            # print(bill_yes)
            # print(bill_no)


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


    def write_db(self):
        """ write data to mongo """

def main():
    p = ProPublica()
    p.get_recent_bills()
    p.get_roll_call()
    results = p.bill_vote_results
    for bill, result in results.items():
        print(f'\n***** Voting results for roll_call vote: {bill} ***** \n')
        print('Yes votes: {}'.format(result['yes']))
        print('No votes: {}'.format(result['no']))


if __name__ == "__main__":
    main()
