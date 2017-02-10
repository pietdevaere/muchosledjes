#!/usr/bin/env python3

##import tweepy
## import re
import json
import time
import socket
import requests
import argparse
import unidecode
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


CONN_FAIL_WAIT_TIME = 10

def url_remover(original):
##    print("in: {}".format(original))
    original = original.split(" ")
    result = ''
##    print (original)
    for word in original:
        if word.find('http') == -1:
            result += word + ' '
##    print("out {}".format(result))
    return result.strip()


class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout. """
    def on_data(self, data):
        priority = 9
        tweet = json.loads(data)
        userID = tweet['user']['id_str']
        lang = tweet['lang']
        text = tweet['text']
        text = unidecode.unidecode(text)
        ##if lang not in langs:
        ##    print ("WRONG LANG: {}".format(text))
        ##    return True
        ## remove urls
        text = url_remover(text)
        if reject and (text.find("RT") != -1 or text.find("http") != -1):
            print ("DROPED: {}".format(text))
            return True
        for user in users:
            if userID == user:
                priority = min(priority, users[user])

        for topic in topics:
            if text.lower().find(topic.lower()) != -1:
                priority = min(priority, topics[topic])
        socketstring = str(priority)+text
        socketbytes = socketstring.encode('ascii')
        sock.sendto(socketbytes, (UDP_IP, UDP_PORT))
        print("Priority {}: {}".format(priority, text))
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':

    ##Parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('topics',
            help='The main keywords to listen to (priority 5)',
            default=[], nargs='*')
    parser.add_argument('-f', '--filler', dest='fillers',
            help='Speccifiy filler topics with minimum priority to listen to (priority 9)',
            default=[], nargs='*')
    parser.add_argument('-d', '--destination', dest='ip',
            help='IP to send the received tweets to',
            default='127.0.0.1')
    parser.add_argument('-p', '--port', dest='port',
            help='port to send the recieved tweets to',
            default=5004, type=int)
    parser.add_argument('--nodrop', dest='reject',
            help="Drop messages containing 'RT' or unfilterable urls",
            default=True, action='store_false') 
    args = parser.parse_args()
    
    ## Read out the twitter keys
    keyFile = open('twitter', 'r')
    consumer_key = keyFile.readline().strip()
    consumer_secret = keyFile.readline().strip()
    access_token = keyFile.readline().strip()
    access_token_secret = keyFile.readline().strip()
    keyFile.close()

    ## The default things to follow
    topics = dict()
    users = {'2625727854':1}
    ##langs = {'en', 'nl', 'fr'}

    ## Add the command line options
    for item in args.topics:
        topics[item] = 5
    for item in args.fillers:
        topics[item] = 9


    trackArray = []
    for topic in topics:
        trackArray.append(topic)

    userArray = []
    for user in users:
        userArray.append(user)

    UDP_IP = args.ip ##"10.23.5.143"
    UDP_PORT = args.port ## 5004
    reject = args.reject

    print("Listening on twitter for:")
    for topic in topics:
        print("\t{:<20} with priority {}".format(topic, topics[topic]))
    for user in users:
        print("\t{:<20} with priority {}".format(user, users[user]))
    if reject: print("filtering out RT and http")
    print("Sending data to {} on port {}".format(UDP_IP, UDP_PORT))

    print('a')
    sock = socket.socket(socket.AF_INET, # Internet
                                 socket.SOCK_DGRAM) # UDP= StdOutListener()

    print('b')
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    print('c')
    l = StdOutListener()

    print('d')
    while True:
        try:
            stream = Stream(auth, l)
            stream.filter(follow=userArray, track=trackArray) #Tomorrowland
        except requests.exceptions.RequestException as e:
            print(e)
            time.sleep(CONN_FAIL_WAIT_TIME)
    print('e')
