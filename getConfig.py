#!/usr/bin/env python3

import requests
import datetime
import dateutil.parser
import os.path

remote_url = "http://kiekehoning.be/bla.txt"
local_url = "/tmp/bla.txt"

def get_local_mtime():
    
    #if the file does not exist
    if not os.path.isfile(local_url):
        return None

    timestamp = os.path.getmtime(local_url)
    mtime = datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)
    
    return mtime

def get_remote_mtime():
    res = requests.request('HEAD', remote_url)
    mtime = dateutil.parser.parse(res.headers['last-modified'])
    
    return mtime

def check_if_remote_is_new():
    return get_remote_mtime() > get_local_mtime()

