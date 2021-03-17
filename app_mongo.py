#!/bin/python3

from datetime import datetime
import pymongo



#VARIAVEIS

conn = pymongo.MongoClient(f'mongodb://192.168.1.29:27017/')

database = conn['fnmdb']


class MongoFindPrefix:
    def __call__(self, net):
        
        y = database['customer'].find_one({'net': f'{net}'}, {'_id':0, 'asn': 1, 'net':1, 'hop':1, 'date':1,})
        if y == None:
            return False
        else:
            return y


