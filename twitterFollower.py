##import tweepy
import json
import socket
import unidecode
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

##auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
##auth.set_access_token(access_token, access_token_secret)


##api = tweepy.API(auth)

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
##        if lang not in langs:
##            print ("WRONG LANG: {}".format(text))
##            return True
        if reject and (text.find("RT") != -1 or text.find("http") != -1):
            print ("DROPED: {}".format(text))
            return True
        for user in users:
            if userID == user:
                priority = min(priority, users[user])

        for topic in topics:
            if text.lower().find(topic.lower()) != -1:
                priority = min(priority, topics[topic])
        sock.sendto(str(priority)+text, (UDP_IP, UDP_PORT))
        print("Priority {}: {}".format(priority, text))
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    
    keyFile = open('twitter', 'r')
    consumer_key = keyFile.readline().strip()
    consumer_secret = keyFile.readline().strip()
    access_token = keyFile.readline().strip()
    access_token_secret = keyFile.readline().strip()
    keyFile.close()

    topics = {'awesome':5, 'ledscherm':3}
    users = {'2625727854':1}
    langs = {'en', 'nl', 'fr'}

    trackArray = []
    for topic in topics:
        trackArray.append(topic)

    userArray = []
    for user in users:
        userArray.append(user)

    UDP_IP = "127.0.0.1"
    UDP_PORT = 5004
    reject = 1

    sock = socket.socket(socket.AF_INET, # Internet
                                 socket.SOCK_DGRAM) # UDP= StdOutListener()

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    l = StdOutListener()

    stream = Stream(auth, l)
##    stream.filter(track=trackArray) #Tomorrowland
    stream.filter(follow=userArray, track=trackArray) #Tomorrowland

