import getpass, poplib
import email
import email.parser
import socket
from unidecode import unidecode
import time

secret = "secreten"


UDP_IP = "127.0.0.1"
UDP_PORT = 5004

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP= StdOutListener()


while True:

    M = poplib.POP3_SSL('pop.gmail.com', 995)
    M.user("muchosledjes")
    M.pass_("ledscherm")
    
    numMessages = len(M.list()[1])
    
    
    
    for msgnr in range(numMessages):
        raw = M.retr( msgnr + 1 )
        msg = email.message_from_string('\n'.join(raw[1]))
        subject =msg.get('Subject') 
        message = msg.as_string()
        if message.find(secret) != -1:
            print("accepted: {}".format(subject))
            sock.sendto('0' + subject, (UDP_IP, UDP_PORT))
        else:
            print("rejected: {}".format(subject))
        ##print(msg.as_string())

    M.quit()
    time.sleep(30)


"""
print(raw)
parser = email.parser.FeedParser()
for line in raw[1]:
        parser.feed( str( line+b'\n') )
        message = parser.close()
"""
"""
numMessages = len(M.list()[1])
for i in range(numMessages):
    parser = email.parser.FeedParser()
    raw = M.retr(i+1)[1]
    for line in raw:
        parser.feed( str( line+b'\n'))
    
    msg = parser.close()
    content = msg.get_payload()
    print (content)
##     for j in M.retr(i+1)[1]:
##            print j

    """
