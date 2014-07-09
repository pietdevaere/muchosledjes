import socket
import time
import math

font = {'A':['01110', '10001', '10001', '10001', '11111', '10001', '10001'],
        'B':['11110', '10001', '10001', '11110', '10001', '10001', '11110'],
        'C':['01110', '10001', '10000', '10000', '10000', '10001', '01110']}

def text_to_bin(text):
    result = ['' for i in range(7)]
    text = text[0:36]  ## truncate the text to the maximum lenght
    for letter in text:
        lenght = 0
        for i in range(7):
            result[i] += font[letter][i] + '0'
            lenght += 1
    return result

def group_to_decimal(group):
    result = 0
    value = 128
    for bit in group:
##        print("  bit = {}, int(bit)= {}, value = {}".format(bit, int(bit), value))
        result += int(bit) * value
        value /= 2
    return result

def bin_to_decarray(binary):
    result = []
    for row in binary:
        groups = [row[i:i+8] for i in range(0, len(row), 8)]
        decrow = []
        for group in groups:
            decrow.append(group_to_decimal(group))
        decrow = decrow + (27 - len(decrow)) * [0] ## pad with zeros
        result.append(decrow)
    return(result)

def decarray_to_bytestream(decarray):
    bytestream = []
    for row in decarray:
        bytestream += row
    print bytestream
    return bytearray(bytestream)
        
            
            

UDP_IP = "10.23.5.143"
UDP_PORT = 5000
MESSAGE = "Hello, World!"

##print "UDP target IP:", UDP_IP
##print "UDP target port:", UDP_PORT
##print "message:", MESSAGE

MESSAGE = decarray_to_bytestream(bin_to_decarray(text_to_bin('ABC'*50)))

sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP


sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
