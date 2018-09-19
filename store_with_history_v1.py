#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 10:08:48 2018

@author: jiaweizhong
"""

import pymongo
import pprint
import datetime

def convert_string_to_time(date_string):
    from datetime import datetime
    date_time_obj = datetime.strptime(date_string[:26], '%Y-%m-%d %H:%M:%S.%f')
    return date_time_obj

def get(db, key):
    obj = db.user.find_one({"name":key})
    if obj == None:
        print('Sorry, we do not have this name in our database.')
        return
    friends_obj = obj[friends]
    friends_list = []
    for friend in friend_obj:
        time_list = friend_obj[friend]
        if len(time_list[1]['remove']) == 0:
            friend_list.append(friend)
        else:
            add_time = convert_string_to_time(time_list[0]['add'][-1])
            remove_time = convert_string_to_time(time_list[1]['remove'][-1])
            if add_time > remove_time:
                friend_list.append(friend)
    return friends_list

def put(db, key, value):
    obj = db.user.find_one({"name":key})
    time = str(datetime.datetime.now())
    if obj == None:
        db.user.insert_one({"name":key, "friends":{value:[{"add":[time]}, {"remove":[]}]}})
    elif value not in obj['friends']:
        obj['friends'].add({value:[{"add":[time]},{"remove":[]}]})
    else:
        obj['friends'][value][0]['add'].append(time)
    return
    
def delete(db, key):
    obj = db.user.find_one({"name":key})
    if obj == None:
        print('Sorry, key is not found.')
    else:
        db.user.delete_one({"name":key})
    return
    
def delete(db, key, value):
    obj = db.user.find_one({"name":key})
    time = str(datetime.datetime.now())
    if obj == None:
        print('Sorry, key is not found.')
    elif value not in obj['friends']:
        print('Sorry, value is not found.')
    else:
        obj['friends'][value][1]['remove'].append(time)
    return 
    
def get(key, time):
    
def diff(key, time1, time2):
    

def main():
    # This is the main function
    # Use pymongo module to connect to db
    client = pymongo.MongoClient()
    db = client.friends

if __name__ == '__main__':
    main()
