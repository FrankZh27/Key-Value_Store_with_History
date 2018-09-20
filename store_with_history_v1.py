#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 10:08:48 2018

@author: jiaweizhong
"""

import pymongo
import datetime
import unittest

def convert_string_to_time(date_string):
# convert string to datatime type, so that we can
# compare two times directly later
    from datetime import datetime
    date_time_obj = datetime.strptime(date_string[:26], '%Y-%m-%d %H:%M:%S.%f')
    return date_time_obj

def put(db, key, value):
# insert a key-value pair in the db. First we need to consider
# if the key exists, then we consider if the value already exists.
# Finally, we consider if the value has been removed before or not.
    obj = db.user.find_one({"name":key})
    time = str(datetime.datetime.now())
    if obj == None:
        db.user.insert_one({"name":key, "friends":{value:[{"add":[time]}, {"remove":[]}]}})
    elif value not in obj['friends']:
        obj['friends'].add({value:[{"add":[time]},{"remove":[]}]})
    elif len(obj['friends'][value][1]['remove']) == 0:
        return
    else:
        last_add = convert_string_to_time(obj['friends'][value][0]['add'][-1])
        last_remove = convert_string_to_time(obj['friends'][value][1]['remove'][-1])
        if last_add <= last_remove:
            obj['friends'][value][0]['add'].append(time)
    return

def delete(db, key, *value):
# Delete the value according to a specific key. First we need to
# consider if the key is already exists, then we consider if the
# value exists.
    if value:
        obj = db.user.find_one({"name":key})
        time = str(datetime.datetime.now())
        if obj == None:
            print('Sorry, key is not found.')
        elif value not in obj['friends']:
            print('Sorry, value is not found.')
        else:
            obj['friends'][value][1]['remove'].append(time)
        return
# Delete the information according to a specific key.
# Here once we delete the key(a user), we destroy everything
# it has. It make sense because if we think of a user deactivating its
# account, all of its information should be removed.
    else:
        obj = db.user.find_one({"name":key})
        if obj == None:
            print('Sorry, key is not found.')
        else:
            db.user.delete_one({"name":key})
        return

def is_there(time, time_list):
# Use this API to consider if a specific value(friend) is in the
# list at current time.
    time_flag = convert_string_to_time(time)
    add_time = time_list[0]['add']
    remove_time = time_list[1]['remove']
    if len(remove_time) == 0:
        return True
    if time_flag < convert_string_to_time(add_time[0]):
        return False
    if time_flag < convert_string_to_time(remove_time[0]):
        return True
    last_add = add_time[0]
    last_remove = remove_time[0]
    for i in range(add_time):
        if convert_string_to_time(add_time[i]) > time_flag:
            last_add = convert_string_to_time(add_time[i-1])
    for i in range(remove_time):
        if convert_string_to_time(remove_time[i]) > time_flag:
            last_remove = convert_string_to_time(remove_time[i-1])
    if last_add <= last_remove:
        return False
    else:
        return True

def get(db, key, *time):   
# Give a list of friends a specific key has.
# When consider if a value in the result list,
# we compare the last insert time and the last
# remove time  
    if time:
        obj = db.user.find_one({"name":key})
        friends_list = []
        if obj == None:
            print('Sorry, key is not found.')
        else:
            for friend in obj['friends']:
                if is_there(time, obj['friends'][friend]):
                    friends_list.append(friend)
        return friends_list
    # Get the friend list according to a speific key
    else:
        obj = db.user.find_one({"name":key})
        if obj == None:
            print('Sorry, we do not have this name in our database.')
            return
        friends_obj = obj['friends']
        friends_list = []
        for friend in friends_obj:
            time_list = friends_obj[friend]
            if len(time_list[1]['remove']) == 0:
                friends_list.append(friend)
            else:
                add_time = convert_string_to_time(time_list[0]['add'][-1])
                remove_time = convert_string_to_time(time_list[1]['remove'][-1])
                if add_time > remove_time:
                    friends_list.append(friend)
        return friends_list
        
    
def diff(db, key, time1, time2):
    list1 = get(db, key, time1)
    list2 = get(db, key, time2)
    set1 = set(list1)
    set2 = set(list2)
    ans = []
    for item in set1:
        if item not in set2:
            ans.append(item)
    for item in set2:
        if item not in set1:
            ans.append(item)
    return ans

class TestAPI(unittest.TestCase):
# This is the unittest module, here I just test two APIs.
# because I changed the time with the actual time at last,
# we can't use integer numbers as timestamps any more
    def test_get(self):
        result = get('A')
        self.assertEqual(result, 'B')
    
    def test_get_with_time(self):
        result = get('A', str(datetime.datetime.now()))
        self.assertEqual(result, 'B')

def main():
    # This is the main function
    # Use pymongo module to connect to db
    client = pymongo.MongoClient()
    db = client.friends
    
    ans = get(db, 'A')
    print(ans)

if __name__ == '__main__':
    main()
    unittest.main()
