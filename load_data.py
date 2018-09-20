#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 22:28:56 2018

@author: jiaweizhong
"""

import pymongo

client = pymongo.MongoClient()
db = client.friends
db.users.insert_one({"name":"A","friends":{"B":[{"add":["0","3"]},{"remove":["1","4"]}],"D":[{"add":["1","3"]},{"remove":["2", "4"]}]}})