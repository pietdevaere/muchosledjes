#!/usr/bin/env python3

from displaytools import *
from sockettools import *
import time
import datetime
import subprocess
import signal
import sys

MSG_PREFIX = '[run.py]: '
child_processes = []

###############################################################################
# start of configuration section
# only edit below this point
###############################################################################

# set the program you want to run
# The options are:
#   - 'twitter' : listen to a twitter feed
#   - 'custom' : run the custom program that is bellow
PROGRAM = 'twitter'

##
## Options for the twitter program
##

# Initial text to show on top row
TWITTER_TWEET_TO_TEXT = 'Tweet naar:'

# Topic to follow on twitter, without '#'
TWITTER_TOPIC = 'boeschrik'            

###############################################################################
# end of configuration section
# do NOT change anything beyond this point, unless you know what you are doing
###############################################################################

###############################################################################
# Definition of the custom program
# You should only change this if you know what you are doing
###############################################################################
def custom():
    social = PriorityReceiver()
    f = Font('ledFont')
    d = Display('127.0.0.1', echo = False)

    while True:
        time.sleep(1)

###############################################################################
# This is the twitter routine. You should NOT change this
###############################################################################
def twitter():
    social = PriorityReceiver()
    f = Font('ledFont')
    d = Display('127.0.0.1', echo = False)
    
    timestamp = datetime.datetime.now().isoformat()
    twitter_output_file = open('log/twitter_'+timestamp, 'w')
    
    # run the twitter receiver
    twitter = subprocess.Popen(['/usr/bin/python3', 'twitterFollower.py', TWITTER_TOPIC],
                                stderr = subprocess.STDOUT,
                                stdout = twitter_output_file)
    child_processes.append(twitter)
    print(MSG_PREFIX + 'Twitter follower started')
    
    
    
    # Set initial text on the display
    StaticRow(d, f, TWITTER_TWEET_TO_TEXT).load(0)
    StaticRow(d, f, '#' + TWITTER_TOPIC).show(1)
    print(MSG_PREFIX + 'Initial text placed on display')
    
    message = None
    priority = None
    
    print(MSG_PREFIX + 'Entering main loop')
    
    while True:
        social.update()
    
        # receive a new message if one is available
        if social.new_messages():
            message, priority = social.pop()
            print(MSG_PREFIX + 'Priority {}:\t {}'.format(priority, message))
        
        else:
            time.sleep(1)
    
        if message != None:
            ScrollText(d, f, message, sleeptime = 0.025).show()


###############################################################################
# This is the twitter routine. You should NOT change this
###############################################################################
def signal_handler(signum, frame):
    print(MSG_PREFIX + 'Received following signal: ', signum)

    if signum == signal.SIGTERM:
        print(MSG_PREFIX + 'Shutting down, goodnight!')
        for child in child_processes:
            child.terminate()
        sys.exit()

if __name__ == '__main__':
	
    signal.signal(signal.SIGTERM, signal_handler)
    
    if PROGRAM == 'twitter':
        twitter()
