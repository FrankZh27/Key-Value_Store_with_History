#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 22:28:56 2018

@author: jiaweizhong
"""

import pymongo

client = pymongo.MongoClient()
db = client.friends
db.users.insert()