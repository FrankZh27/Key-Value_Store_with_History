#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 05:07:34 2018

@author: jiaweizhong
"""

def convert_string_to_time(date_string):
    from datetime import datetime
    date_time_obj = datetime.strptime(date_string[:26], '%Y-%m-%d %H:%M:%S.%f')

    return date_time_obj

date = '2018-08-14 13:09:24.543953'
date_time_obj_timezone = convert_string_to_time(date)
