#!/usr/bin/env python


class ProPublica:
    def __init__(self):
        pass

    def authenticate(self):
        """
        build authentication header request and endpoint using the instructions at:
        https://projects.propublica.org/api-docs/congress-api/#authentication

        """

    def get_recent_bills(self):
        """ connect to bill endpoint to get 20 most recent bills """
        # GET https://api.propublica.org/congress/v1/{chamber}/votes/recent.json

    def get_roll_call(self):
        """ connect to vote endpoint to get roll call votes for all recent bills
        GET https://api.propublica.org/congress/v1/{congress}/{chamber}/sessions/{session-number}/votes/{roll-call-number}.json
        """

        """ pseudo code
        
        for bill in bills:
            get_roll_call(bill)
        
        """

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

        """ pseudo code 
        
        bill_results = []
        
        for vote in votes:
            bill_id = vote['bill']['bill_id']
            title = vote['bill']['title']
            ...
            d_votes = (vote['democratic']['yes'], vote['democratic']['no'])  # tuple
            
            bill_results.append(vote) 
            
        df = DataFrame.from_records(bill_results)
        
        """

    def write_db(self):
        """ write data to mongo """

def main():
    pass


if __name__ == "__main__":
    main()
