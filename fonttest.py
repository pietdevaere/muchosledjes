import socket
import time
import math


def text_to_bin(text):
    """Converts text to 7 rows of binary data, 1 represents a lit pixel"""

    result = ['' for i in range(7)]
    text = text[0:36]  ## truncate the text to the maximum lenght
    for letter in text:
        lenght = 0
        for i in range(7):
            result[i] += font[letter][i] + '0'
            lenght += 1
    return result

def group_to_decimal(group):
    """Converts a group of 8 binary digits to it's decimal value, outdated"""
    result = 0
    value = 128
    for bit in group:
        result += int(bit) * value
        value /= 2
    return result

def bin_to_decarray(binary):
    result = []
    for row in binary:
        groups = [row[i:i+8] for i in range(0, len(row), 8)]
        decrow = []
        for group in groups:
            decrow.append(int(group, 2))
         ##   decrow.append(group_to_decimal(group))
        decrow = decrow + (27 - len(decrow)) * [0] ## pad with zeros
        result.append(decrow)
    return(result)

def decarray_to_bytestream(decarray):
    bytestream = []
    for row in decarray:
        bytestream += row
##    print bytestream
    return bytearray(bytestream)

def static_text(message, quite = 0):
    if len(message) > 36 and quite == 0:
        print("Message to long, will be shorted")
    frame = decarray_to_bytestream(bin_to_decarray(text_to_bin(message)))

    sock = socket.socket(socket.AF_INET, # Internet
        socket.SOCK_DGRAM) # UDP
    sock.sendto(frame, (UDP_IP, UDP_PORT))

def scrolling_text(message):
    pass    


font = {' ':['00000', '00000', '00000', '00000', '00000', '00000', '00000']}

fontFile = open('ledFont', 'r')

for line in fontFile:
    line = line.strip()
    line = line.split(' ')
    font[line[0]] = line[1:][::-1]

fontFile.close()

UDP_IP = "10.23.5.143"
UDP_PORT = 5000
MESSAGE = "Hello, World!"

##print "UDP target IP:", UDP_IP
##print "UDP target port:", UDP_PORT
##print "message:", MESSAGE

static_text('The quick brown fox jumps over the lazy dog')
