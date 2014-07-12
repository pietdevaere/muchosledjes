import socket
import time
import math

def text_to_bin(text):
    """Converts text to 7 rows of binary data, 1 represents a lit pixel"""

    result = ['' for i in range(LINES)] ##e every string represents a ledrow
    for letter in text:
        lenght = 0
        for i in range(LINES):
            try: ## look up the letter in the fontlist
                result[i] += font[letter][i] + '0' ## and add it to the string
            except KeyError: ## for an unkown symbol, insert '?'
                result[i] += font[letter][i] + '0'
            lenght += 1
    return result

def bin_to_decarray(binary):
    """converts the array of 7 rows of binary data to an array with seven arrays of bytes"""
    result = []
    for row in binary:
        ## split up the string in groups of eight bits
        groups = [row[i:i+8] for i in range(0, len(row), 8)]
        decrow = []
        for group in groups: ## convert each group to an integer
            while len(group) < 8:  ## pad with zeros for the int conversion function
                group += '0'
            decrow.append( int(group, 2) )
        decrow = decrow + (BYTESONLINE - len(decrow)) * [0] ## pad with zeros
        result.append(decrow)
    return(result)

def decarray_to_bytestream(decarray):
    """takes as input an array of arrays of bytes, and outputs the bytestream for the display"""
    bytestream = []
    for row in decarray: ## for every row, add the relavants bytes to the bytestream
        bytestream += row[:BYTESONLINE] ## ignore the others
    return bytearray(bytestream)

def static_text(message, quiet = 0):
    """shows a static text message on the display"""
    if len(message) > 36 and quiet == 0:
        print("Message to long, will be shorted")
    message = message[0:36]  ## truncate the text to the maximum lenght
    frame = decarray_to_bytestream(bin_to_decarray(text_to_bin(message)))
    transmit(frame)


def transmit(bytestream = None):
    """send a frame to the display driver"""
    if bytestream == None:
        sock.sendto(displayData, (UDP_IP, UDP_PORT))
    else:
        sock.sendto(bytestream, (UDP_IP, UDP_PORT))


def scrolling_text(message, sleeptime = 0.1, delta = 1):
    """Displays a scrolling text"""
    rowData = text_to_bin(message)
    for i in range(len(rowData)): ## pad the message with empty space front and back
        rowData[i] = 216*'0' + rowData[i] + 216*'0'
    while len(rowData[0]) >= 216: ## now roll through the data
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
    """Clears the display"""
    static_text('', 1)

def split_to_lines(message):
    """Splits the messages on word base into strings that fit on a single line"""
    result = []
    words = message.split()
    line = ''
    lineChars = 0

    ## as long as we haven't procesed the entire message
    while len(words) > 0:
        ## if another word fits on a line
        if lineChars + len(words[0]) < CHARSONLINE:
            lineChars += len(words[0])
            line += words.pop(0)
            if lineChars < CHARSONLINE:
                line += ' '
                lineChars += 1
        
        ## if the next word is to long to fit on an empty line
        elif len(words[0]) > CHARSONLINE and len(line) < CHARSONLINE:
            charsToShow = CHARSONLINE - lineChars
            line += words[0][:charsToShow]
            words[0] = words[0][charsToShow:]
            lineChars = CHARSONLINE

        ## otherwise create a new line
        else:
            result.append(line)
            line = ''
            lineChars = 0

    ## add the last line to the array
    result.append(line)
    return result

def display_on_line(message, line, transmit = 1):
    pass

def gen_disp_data(rowData = rowData):
    """convert the rowData to a bytestream displayData"""
    decArray = [[] for i in range(LINES)]]
    for row in range(ROWS):
        for line in range(LINES):
            decArray[LINES].append(
                rowData[row][line])
    global displayData
    displayData = decarray_to_bytestream(decArray)
    return displayData

font = {' ':['00000', '00000', '00000', '00000', '00000', '00000', '00000']}

fontFile = open('ledFont', 'r')

for line in fontFile:
    line = line.strip()
    line = line.split(' ')
    font[line[0]] = line[1:][::-1]

fontFile.close()

## some constants
UDP_IP = "10.23.5.143"
UDP_PORT = 5000
MESSAGE = "Hello, World!"
CHARSONLINE = 16
BYTESONLINE = 27
LINES = 7
ROWS = 2
BYTES = BYTESONLINE * LINES

## global variables
displayData = [0 for i in range(BYTES)] ## bytestream for the display
rowData = [[[0 for i in range(BYTESONLINE/2)] for k in range(LINES)] for j in range(2)]

sock = socket.socket(socket.AF_INET, # Internet
    socket.SOCK_DGRAM) # UDP

sleep = time.sleep


static_text('boe!')
##time.sleep(3)
static_text('schrik?')
##time.sleep(3)
static_text('#hastag')
##time.sleep(5)
##blink_text('Hallo, ik ben een flikkerlichtje', 10, 0.3, 0.2)
##scrolling_text('Ahoi, ik ben een heeele lange scrollende tekst, maar dan ook echt heeeel lang eh!', 0.05, 1)
