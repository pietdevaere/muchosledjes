import socket
import time
import math

def text_to_bin(text):
    """Converts text to 7 rows of binary data, 1 represents a lit pixel"""

    result = ['' for i in range(7)]
    for letter in text:
        lenght = 0
        for i in range(7):
            try:
                result[i] += font[letter][i] + '0'
            except KeyError:
                result[i] += font[letter][i] + '0'
            lenght += 1
    return result

def bin_to_decarray(binary):
    """converts the array of 7 rows of binary data to an array with seven arrays of bytes"""
    result = []
    for row in binary:
        groups = [row[i:i+8] for i in range(0, len(row), 8)]
        decrow = []
        for group in groups:
            while len(group) < 8:  ## pad with zeros for the int conversion function
                group += '0'
            decrow.append( int(group, 2) )
        decrow = decrow + (27 - len(decrow)) * [0] ## pad with zeros
        result.append(decrow)
    return(result)

def decarray_to_bytestream(decarray):
    """takes as input an array of arrays of bytes, and outputs the bytestream for the display"""
    bytestream = []
    for row in decarray:
        bytestream += row[:27]
    return bytearray(bytestream)

def static_text(message, quiet = 0):
    """shows a static text message on the display"""
    if len(message) > 36 and quiet == 0:
        print("Message to long, will be shorted")
    message = message[0:36]  ## truncate the text to the maximum lenght
    frame = decarray_to_bytestream(bin_to_decarray(text_to_bin(message)))
    transmit(frame)

def transmit(bytestream):
    sock.sendto(bytestream, (UDP_IP, UDP_PORT))


def scrolling_text(message, sleeptime = 0.1, delta = 1):
    """Displays a scrolling text"""
    rowData = text_to_bin(message)
    for i in range(len(rowData)):
        rowData[i] = 216*'0' + rowData[i] + 216*'0'
    while len(rowData[0]) >= 216:
        frame = decarray_to_bytestream(bin_to_decarray(rowData))
        transmit(frame)
        for i in range(len(rowData)):
            rowData[i] = rowData[i][delta:]
        time.sleep(sleeptime)

def blink_text(message, numberOfBlinks, showTime, hideTime = None):
    """Displays a blinking text"""
    if hideTime == None:
        hideTime = showTime
    for i in range(numberOfBlinks):
        print("Blink nr {} of {}".format(i + 1, numberOfBlinks))
        static_text(message, 1)
        time.sleep(showTime)
        static_text('', 1)
        time.sleep(hideTime)

def clear_screen():
    static_text('', 1)

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

sock = socket.socket(socket.AF_INET, # Internet
    socket.SOCK_DGRAM) # UDP

sleep = time.sleep

static_text('ik ben gewoon een statische tekst')
time.sleep(5)
static_text('boe!')
time.sleep(3)
static_text('schrik?')
time.sleep(3)
static_text('#hastaging')
time.sleep(5)
blink_text('Hallo, ik ben een flikkerlichtje', 10, 0.3, 0.2)
scrolling_text('Ahoi, ik ben een heeele lange scrollende tekst, maar dan ook echt heeeel lang eh!', 0.05, 1)