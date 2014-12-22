import socket
import time
import math
from PIL import Image
import numpy

def text_to_bin(text):
    """Converts text to 7 rows of binary data, 1 represents a lit pixel"""
    result = ['' for i in range(LINES)] ##e every string represents a ledrow
    for letter in text:
        lenght = 0
        for i in range(LINES):
            try: ## look up the letter in the fontlist
                result[i] += font[letter][i] + '0' ## and add it to the string
            except KeyError: ## for an unkown symbol, insert '?'
                result[i] += font['?'][i] + '0'
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
    if len(message) > CHARSONDISP and quiet == 0:
        print("Message to long, will be shorted")
    message = message[:CHARSONDISP]  ## truncate the text to the maximum lenght
    frame = decarray_to_bytestream(bin_to_decarray(text_to_bin(message)))
    transmit(frame)


def transmit(bytestream = None):
    """send a frame to the display driver"""
    if bytestream == None:
        display.sendto(displayData, (DISP_IP, DISP_PORT))
    else:
        display.sendto(bytestream, (DISP_IP, DISP_PORT))


def scrolling_text(message, sleeptime = 0.1, delta = 1):
    """Displays a scrolling text"""
    global displayData
    binData = text_to_bin(message)
    for i in range(len(binData)): ## pad the message with empty space front and back
        binData[i] = 216*'0' + binData[i] + 216*'0'
    while len(binData[0]) >= 216: ## now roll through the data
        displayData = decarray_to_bytestream(bin_to_decarray(binData))
        transmit(displayData)
        for i in range(len(binData)):
            binData[i] = binData[i][delta:]
        time.sleep(sleeptime)

def blink_text(message, numberOfBlinks, showTime, hideTime = None):
    """Displays a blinking text"""
    if hideTime == None:
        hideTime = showTime

    message = split_to_lines(message)
    for i in range(numberOfBlinks):
        print("Blink nr {} of {}".format(i + 1, numberOfBlinks))
        display_on_line(message[0], 0, 0)
        display_on_line(message[1], 1, 1)
        time.sleep(showTime)
        static_text('', 1)
        time.sleep(hideTime)

def clear_screen():
    """Clears the display"""
    static_text('', 1)

def fill_screen():
    """ Light up the entire display """
    global rowData
    rowData = [['1'*LEDSONROW for k in range(LINES)] for j in range(ROWS)]
    gen_disp_data()
    transmit()

def flicker(numberOfFlickers = 1, showTime = 0.1, hideTime = None):
    """Make the display flicker"""
    if hideTime == None:
        hideTime = showTime
    for i in range(numberOfFlickers):
        fill_screen()
        time.sleep(showTime)
        clear_screen()
        time.sleep(hideTime)

def split_to_lines(message):
    """Splits the messages on word base into strings that fit on a single line"""
    result = []
    words = message.split()
    line = ''
    lineChars = 0

    ## as long as we haven't procesed the entire message
    while len(words) > 0:
        ## if another word fits on a line
        if lineChars + len(words[0]) < CHARSONROW:
            lineChars += len(words[0])
            line += words.pop(0)
            if lineChars < CHARSONROW:
                line += ' '
                lineChars += 1
        
        ## if the next word is to long to fit on an empty line
        elif len(words[0]) > CHARSONROW and len(line) < CHARSONROW:
            charsToShow = CHARSONROW - lineChars
            line += words[0][:charsToShow]
            words[0] = words[0][charsToShow:]
            lineChars = CHARSONROW

        ## otherwise create a new line
        else:
            result.append(line)
            line = ''
            lineChars = 0

    ## add the last line to the array
    result.append(line)
    return result

def display_on_line(message, row = 0, trans = 1, center = 1):
    global rowData
    message = message[:CHARSONROW]
    binData = text_to_bin(message)
    if center == 1:
        binData = center_bin(binData)
    rowData[row] = binData
    gen_disp_data()
    if trans == 1:
        transmit()

def gen_disp_data():
    """convert the rowData to a bytestream displayData"""
    decArray = ['' for i in range(LINES)]
    for row in range(ROWS):
        for line in range(LINES):
            paddedData = '{:0<108}'.format(rowData[row][line][:LEDSONROW])
            decArray[line] += paddedData
    global displayData
    displayData = decarray_to_bytestream(bin_to_decarray(decArray))

    return displayData

def display_all(message, sleepTime = 3, center = 1):
    message = split_to_lines(message)
    row = 0
    while message:
        display_on_line(message.pop(0), row, row, center)
        if row:
            time.sleep(sleepTime)
    row = not row
    if row:
        display_on_line('', row, row)
        time.sleep(sleepTime)

def scroll_row(message, row = 0,  sleeptime = 0.1, delta = 1):
    """Displays a scrolling text on a specified row"""
    global rowData
    binData = text_to_bin(message)
    for i in range(len(binData)): ## pad the message with empty space front and back
        binData[i] = 108*'0' + binData[i] + 108*'0'
    while len(binData[0]) >= 108: ## now roll through the data
        rowData[row] = binData[:108]
        gen_disp_data()
        transmit()
        for i in range(len(binData)):
            binData[i] = binData[i][delta:]
        time.sleep(sleeptime)

def center_bin(binData):
    ## first strip of any padding from the data
    done = 0
    while not done: ## from the beginning
        front = 1
        back = 1
        for i in range(len(binData)):
            if not binData[1]:
                front = back = 0
            if front and  binData[i][0] == '1':
                front = 0
            if back  and  binData[i][-1] == '1':
                back = 0
        if front:
            for i in range(len(binData)):
                binData[i] = binData[i][1:]
        if back:
            for i in range(len(binData)):
                binData[i] = binData[i][:-1]
        else:
            done = 1

    ## now pad left and right untill we are done
    while len(binData[0]) + 2 < LEDSONROW:
        for i in range(len(binData)):
            binData[i] = '0' + binData[i] + '0'
    if len(binData[0]) < LEDSONROW:
        for i in range(len(binData)):
            binData[i] += '0'

    return binData

def displayImage(path, row = 0):
    size = (LEDSONLINE, LINES)
    im = Image.open(path).convert("L")
    im.resize(size, Image.ANTIALIAS)
    arr = numpy.array(im)

    binData = ['' for i in range(LINES)]
    for line in range(LINES):
        for pixel in arr[line]:
            if pixel < 128:
                binData[line] += '1'
            else:
                binData[line] += '0'
    rowData[row] = binData
    gen_disp_data()
    transmit()

def get_incomming():
    global messageBuffer
    while True:
        try:
            data, addr = incomming.recvfrom(1024, socket.MSG_DONTWAIT)
            data = data.strip()
            try:
                priority = int(data[0])
            except ValueError:
                priority = 0
 ##               print("received bad package: {}".format(data))
 ##               continue
            message = data[1:].replace('\n', ' ')
            messageBuffer[priority].append(message)
            if len(messageBuffer[priority]) > 1000:
                messageBuffer[priority] = messageBuffer[priority][len(messageBuffer[priority])-1000:1000]
        except socket.error:
            break

def buf_empty():
    empty = 1
    for el in messageBuffer:
        if el:
            empty = 0
    return empty


font = {' ':['00000', '00000', '00000', '00000', '00000', '00000', '00000'],
        '\n':['00000', '00000', '00000', '00000', '00000', '00000', '00000']}
fontFile = open('ledFont', 'r')

for line in fontFile:
    line = line.strip()
    line = line.split(' ')
    font[line[0]] = line[1:][::-1]

fontFile.close()

## some constants
DISP_IP = "127.0.0.1" ##"12.23.5.143"
DISP_PORT = 5000
INC_IP = ""
INC_PORT = 5004
CHARSONROW = 18
CHARSONDISP = 36
LEDSONLINE = 216
LEDSONROW = LEDSONLINE/2
BYTESONLINE = 27
LINES = 7
ROWS = 2
BYTES = BYTESONLINE * LINES

## global variables
displayData = [0 for i in range(BYTES)] ## bytestream for the display
rowData = [['' for k in range(LINES)] for j in range(ROWS)]
messageBuffer = [[] for i in range(10)]
display = socket.socket(socket.AF_INET, # Internet
          socket.SOCK_DGRAM) # UDP

incomming = socket.socket(socket.AF_INET, # Internet
            socket.SOCK_DGRAM) # UDP

incomming.bind((INC_IP, INC_PORT))

sleep = time.sleep

## display_on_line("#hashtag", 0)
changed = 1

flicker(1000, 0.05)

"""
while True:
    get_incomming()
    if changed and buf_empty():
        display_on_line("Tweet to", 0, 0)
        display_on_line("#woesh", 1, 1)
        changed = 0
    for prior in range(10):
        if messageBuffer[prior]:
            changed = 1
            message = messageBuffer[prior].pop()
            print("Priority {}: {}".format(prior, message))
            scroll_row(message, 0, 0.025)
            break
<<<<<<< HEAD

=======
>>>>>>> d436a7f
displayImage("fig/test5.jpg", 0)
time.sleep(5)

display_all("Loremipsumdolorsitamet, consectetur adipiscing elit. Praesent non consectetur mi. Vestibulum nisl erat, pretium et augue quis, egestas laoreet odio. Phasellus lacinia magna orci, eu porttitor"
        , 2)

display_on_line('ping pong ping pong ping pong ping', 0, 0)
display_on_line('balletje', 1)
time.sleep(3)
display_on_line('boe!')

time.sleep(3)
clear_screen()
time.sleep(3)
display_on_line('#hashtag', 1)
time.sleep(5)
blink_text('Hallo, ik ben een flikkerlichtje', 10, 0.3, 0.2)
display_on_line('#hashtag', 1, 0)
scroll_row('Ahoi, ik ben een heeele lange scrollende tekst, maar dan ook echt heeeel lang eh!', 0, 0.05)
"""
