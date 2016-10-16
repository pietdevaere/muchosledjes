#!/usr/bin/env python3

import requests
import datetime
import dateutil.parser
import os.path
import os
import urllib.request
import subprocess
import sys
import time
import shutil
import signal

SERVER_URL = "http://kiekehoning.be/bla.py"
LOCAL_URL = "/tmp/bla.py"
POLLING_TIME = 60


class File():
    def __init__(self,  url):
        self.url = url

    def get_url(self):
        return self.url

class LocalFile(File):
    def mtime(self):
        #if the file does not exist
        if not self.exists():
            return None
        
        timestamp = os.path.getmtime(self.url)
        mtime = datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)
        return mtime

    def get(self, destination):
       shutil.copyfile(self.url, destination)

    def exists(self):
        return os.path.isfile(self.url)
        

class HttpFile(File):
    def mtime(self):
        try:
            res = requests.request('HEAD', self.url)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            return None

        if res.status_code == 200:
            try:
                mtime = dateutil.parser.parse(res.headers['last-modified'])
            except KeyError:
                return None
            return mtime

        return None
        
    def get(self, destination):
        try:
            print('--> Trying to get the file over HTTP')
            urllib.request.urlretrieve(self.url, destination)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            print(e)
            return False
        else:
            return True
                                        
class MonitoredFile():
    def __init__(self, source_file):
        self.file = source_file
        self.sources = []

    def add_source(self, source_file):
        self.sources.append(source_file)
   
    def get_latest_source(self):
        latest_mtime = self.file.mtime()
        latest_source = None

        for source in self.sources:
            source_mtime = source.mtime()
            if source_mtime == None:
                continue
            if source_mtime > latest_mtime:
                latest_mtime = source_mtime
                latest_source = source

        if latest_source != None:
            print('--> Found a newer version of the file!')
            print('--> at path: ' + latest_source.get_url())

        return latest_source

    def update(self):
        source = self.get_latest_source()
        if source:
            source.get(self.get_url())
            os.chmod(self.get_url(), 0o744)
                
    def exists(self):
        return True 

    def get_url(self):
        return self.file.get_url()

class Process():
    def __init__(self, executable):
        self.executable = executable
        self.start_time = None
        self.process = None

    def run_latest(self):
        if not self.executable.exists():
            return

        if self.start_time == None or self.executable.mtime() > self.start_time:
            print('--> File changed, restarting')
            self.kill()  # beter be safe!
            self.start_time = datetime.datetime.now(tz=datetime.timezone.utc)
            self.start()            

    def start(self):
        self.process = subprocess.Popen(self.executable.get_url())

    def kill(self):
        if self.process:
            self.process.kill()

child_process = None

def signal_handler(signum, frame):
    print('Received following signal: ', signum)
    
    if signum == signal.SIGTERM:
        print('Shutting down, goodnight!')
        if child_process:
            child_process.kill()
        sys.exit()

if __name__ == "__main__":

    signal.signal(signal.SIGTERM, signal_handler)

    process_file = MonitoredFile(LocalFile(LOCAL_URL))
    process_file.add_source(HttpFile(SERVER_URL))
    process_file.add_source(LocalFile('/tmp/blo.py')) 
    process = Process(LocalFile(LOCAL_URL))
    child_process = process

    try:
        while True:
            process_file.update()
            process.run_latest()
            time.sleep(1)
    except:
        raise
    finally:
        process.kill()
    
    sys.exit()
