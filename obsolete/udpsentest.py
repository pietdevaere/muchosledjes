import socket
import time
import math

UDP_IP = "10.23.5.143"
UDP_PORT = 5000
MESSAGE = "Hello, World!"

##print "UDP target IP:", UDP_IP
##print "UDP target port:", UDP_PORT
##print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP

MESSAGE = bytearray([0])

while True:
    for i in range(8):
        MESSAGE = bytearray([int(math.pow(2,i))]*189)
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        time.sleep(0.05)
