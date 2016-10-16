#!/usr/bin/env python3

from displaytools import *
from sockettools import *
import time
import datetime
import subprocess

###############################################################################
# start of configuration section
# only edit below this point
###############################################################################

# Initial text to show on top row
TWEET_TO_TEXT = 'Tweet naar:'

# Topic to follow on twitter, without '#'
TOPIC = 'EmiEnEpi'            

# Speed to scroll text at.
# Default: 0.025, smaler is faster
SCROLL_SPEED = 0.025            

###############################################################################
# end of configuration section
# do NOT change anything beyond this point
###############################################################################

social = PriorityReceiver()
f = Font('ledFont')
d = Display('127.0.0.1', echo = False)

timestamp = datetime.datetime.now().isoformat()
twitter_output_file = open('log/twitter_'+timestamp, 'w')

# run the twitter receiver
twitter = subprocess.Popen('python3 twitterFollower.py ' + TOPIC,
                            shell = True,
                            stderr = subprocess.STDOUT,
                            stdout = twitter_output_file)
print('--> Twitter follower started')



# Set initial text on the display
StaticRow(d, f, TWEET_TO_TEXT).load(0)
StaticRow(d, f, '#' + TOPIC).show(1)
print('--> Initial text placed on display')

message = None
priority = None

print('--> Entering main loop')

while True:
    social.update()

    # receive a new message if one is available
    if social.new_messages():
        message, priority = social.pop()
        print('Priority {}:\t {}'.format(priority, message))
    
    else:
        time.sleep(1)

    if message != None:
        ScrollText(d, f, message, sleeptime = 0.025).show()
