#!/usr/bin/env python

import sys
import json


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


def write_json(data, **args):
    if args.get('senators'):
        print("\n***** wrote senators *****")
        with open('data/senators.json', 'w') as f:
            for d in data:
                f.write(json.dumps(d) + '\n')
    elif args.get('bill'):
        print("***** wrote votes *****")
        with open('data/votes.json', 'w') as f:
            for d in data:
                f.write(json.dumps(d) + '\n')

    elif args.get('tally'):
        print("***** wrote tally *****")
        with open('data/tally.json', 'w') as f:
            for d in data:
                f.write(json.dumps(d) + '\n')
    else:
        print("***** wrote roll_call *****")
        with open('data/roll_call.json', 'w') as f:
            for d in data:
                f.write(json.dumps(d) + '\n')


def load_json():
    with open('data/senators.json', 'r') as a:
        senators = [json.loads(x) for x in a.readlines()]
    with open('data/votes.json', 'r') as b:
        votes = [json.loads(x) for x in b.readlines()]
    with open('data/roll_call.json', 'r') as c:
        roll_call = [json.loads(x) for x in c.readlines()]
    with open('data/tally.json', 'r') as d:
        tally = [json.loads(x) for x in d.readlines()]

    return senators, votes, roll_call, tally

