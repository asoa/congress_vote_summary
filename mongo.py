#!/usr/bin/env python

from pymongo import MongoClient


class mongo:
    def __init__(self, **kwargs):
        self.kwargs = {k:v for k,v in kwargs.items()}
        self.do_init = self.kwargs.get('do_init', False)
        self.client = self.client = MongoClient('0.0.0.0', 27017)
        if self.do_init:
            self.init()

    def init(self):
        """ intitialize mongo db and collection"""
        db = self.client.congress
        coll_bills = db.bills
        coll_roll_call = db.roll_call
