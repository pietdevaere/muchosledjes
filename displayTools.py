import socket
import time
import math
from PIL import Image
import numpy

class Display():
    """ A class that handles the communication with the display """
    chars_on_row = 18
    chars_on_disp = 36
    leds_on_line = 216
    leds_on_row = leds_on_line//2
    bytes_on_line = 27
    lines = 7
    rows = 2
    total_bytes = bytes_on_line*lines

    def __init__(self, ip = '127.0.0.1', port = 5000):
        self.ip = ip
        self.port = port
        ## open a udp socket
        self.socket = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP
        ## binary display data
        row_data = [["0"*self.leds_on_row for k in range(self.lines)]
                for j in range(self.rows)]
        ## bytestream to be send to the diplay
        bytestream = [0 for i in range(self.total_bytes)]

    def __repr__(self):
        self.pad_row_data()
        result = ''
        for row in range(self.rows):
            for line in range(self.lines):
                result += self.row_data[row][line] + '\n'
            result += '\n'
        result = result.replace('1', chr(9608))
        result = result.replace('0', ' ')
        return(result)
        
    def pad_row_data(self):
        for row in range(self.rows):
            for line in range(self.lines):
                self.row_data[row][line] = '{:0<108}'.format(
                        self.row_data[row][line][:self.leds_on_row])

    def transmit(self):
        """Send the current frame to the display"""
        self.socket.sendto(self.bytestream, (self.ip, self.port))

    def gen_bytestream(self):
        """Create the bytestream from row_data"""
        self.pad_row_data()
        ## array where the two rows of a line are next to each other
        long_line_array = ['' for i in range(self.lines)]
        for row in range(self.rows):
            for line in range(self.lines):
                long_line_array[line] += self.row_data[row][line]
        self.bytestream = self.bytearray_to_bytestream(
                self.bin_to_bytearray(long_line_array))

    def update(self):
        self.gen_bytestream()
        self.transmit()
    
    def bin_to_bytearray(self, binary):
        """converts the array of 7 rows of binary data
            to an array with seven arrays of bytes"""
        result = []
        for row in binary:
            ## split up the binary array in to groups of eight bits
            groups = [row[i:i+8] for i in range(0, len(row), 8)]
            byte_row = []
            ## Now convert every group to an integer
            for group in groups:
                ## padd with zeros for int convertion function
                while len(group) < 8:
                    group += '0'
                byte_row.append(int(group, 2))
                ## pad with zeros to apropriate lenght
            byte_row = byte_row + (self.bytes_on_line - len(byte_row)) * [0]
            result.append(byte_row)
        return(result)

    def bytearray_to_bytestream(self, byte_array):
        """takes as input an array of arrays of bytes
            and outputs the bytestream for the display"""
        result = []
        for row in byte_array:
            result += row[:self.bytes_on_line] # limit to display size
        return(bytearray(result))

    def clear(self):
        self.row_data = [['0'*self.leds_on_row for k in range(self.lines)]
                for j in range(self.rows)]
        self.update()

    def fill(self):
        self.row_data = [['1'*self.leds_on_row for k in range(self.lines)]
                for j in range(self.rows)]
        self.update()

class TextEffect():
    """ A class that holds an effect generator """
    

d = Display('10.23.5.143')
d.fill()
time.sleep(1)
d.clear()
time.sleep(1)
d.fill()
print(d)
        
    




