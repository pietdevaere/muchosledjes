import socket
import time
import math
from PIL import Image
import numpy

class Display(object):
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
        self.row_data = [["0"*self.leds_on_row for k in range(self.lines)]
                for j in range(self.rows)]
        ## bytestream to be send to the diplay
        self.bytestream = [0 for i in range(self.total_bytes)]

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

    def clear(self, update = True):
        self.row_data = [['0'*self.leds_on_row for k in range(self.lines)]
                for j in range(self.rows)]
        if update:
            self.update()

    def fill(self, update = True):
        self.row_data = [['1'*self.leds_on_row for k in range(self.lines)]
                for j in range(self.rows)]
        if update:
            self.update()

    def load_row(self, single_row_data, row = 0):
        self.row_data[row] = single_row_data[:]


class Font(object):
    """ A class to store a font """
    font = {' ':['00000', '00000', '00000', '00000', '00000', '00000', '00000'],
           '\n':['00000', '00000', '00000', '00000', '00000', '00000', '00000']}

    def __init__(self, font_file_path):
        font_file = open(font_file_path)
        for line in font_file:
            line = line.strip().split(' ')
            self.font[line[0]] = line[1:][::-1]
        font_file.close()

    def __getitem__(self, key):
        return self.font[key]

class Effect(object):
    pass

class TextEffect(Effect):
    """ A class that holds an effect generator """
    def __init__(self, display, font, dynamic, text):
        self.text = text
        self.d = display
        self.f = font
        self.dynamic = dynamic
    

    def text_to_bin(self, text = None):
        """Converts text to 7 rows of binary data, 1 represents a lit pixel"""
        if text is None:
            text = self.text
        result = ['' for i in range(self.d.lines)]
        for letter in text:
            for i in range(self.d.lines):
                try:
                    result[i] += self.f[letter][i] + '0' # Add a whitespace
                except KeyError: # Charachter not in fontset
                    result[i] += self.f[' '][i] + '0'
        return result

    def split_to_lines(self, text = None):
        """Splits self.text into mutliple stings that fit on one line
            returns an array of these strings"""
        if text is None:
            text = self.text
        result = []
        words = text.split()
        line = ''
        line_chars = 0

        while words:
            ## if the line is not full yet, add a word
            if line_chars + len(words[0]) < self.d.chars_on_row:
                line_chars += len(words[0])
                line += words.pop(0)
                ## if it is still not full, add a whitespace
                if line_chars < self.d.chars_on_row:
                    line += ' '
                    line_chars += 1

            ## if the next word is to long to fit on an empty line
            elif (len(words[0]) > self.d.chars_on_row
                    and len(line) < self.d.chars_on_row):
                chars_to_show = self.d.chars_on_line - lineChars
                line += words[0][:chars_to_show]
                words[0] = words[0][chars_to_show]
                line_chars = self.d.chars_on_row

            ## otherwise: create a new line
            else:
                result.append(line)
                line = ''
                line_chars = 0

        result.append(line) # add the last line
        return result

    def center_bin_array(self, bin_array):
        result = []

        ## First strip away any spacing.
        done = False
        while not done:
            front = True
            back = True
            if not bin_array[0]: # if there is notting left in the string
                front = back = False
            ## check if there are empty spaces front or back
            for i in range(len(bin_array)):
                if front and bin_array[i][0] == '1':
                    front = False
                if back and bin_array[i][-1] == '1':
                    back = False

            if front: # remove empty space from front
                for i in range(len(bin_array)):
                    bin_array[i] = bin_array[i][1:]
            if back: # remove empty space from back
                for i in range(len(bin_array)):
                    bin_array[i] = bin_array[i][:-1]
            else:
                done = True

        ## Now pad left and right
        while len(bin_array[0]) + 2 < self.d.leds_on_row:
            for i in range(len(bin_array)):
                bin_array[i] = '0' + bin_array[i] + '0'
        if len(bin_array[0]) < self.d.leds_on_row:
            for i in range(len(bin_array)):
                bin_array[i] += '0'

        return bin_array

class StaticRow(TextEffect):
    """Display static text on a single row"""
    def __init__(self, display, font, text, justify = 'center'):
        super().__init__(display, font, False, text)
        self.bin_array = self.text_to_bin()
        if justify is 'center':
            self.bin_array = self.center_bin_array(self.bin_array)
    
    def load(self, row = 0):
        self.d.load_row(self.bin_array, row)
    
    def show(self, row = 0):
        self.load(row)
        self.d.update()

class StaticDisplay(TextEffect):
    def __init__(self, display, font,  text, justify = 'center'):
        super().__init__(display, font, False, text)
        self.text_rows = self.split_to_lines()
        self.rows_to_show = min(len(self.text_rows), self.d.rows)
        self.bin_array = []
        for i in range(self.rows_to_show):
            row_bin_array = self.text_to_bin(self.text_rows[i])
            if justify is 'center':
                row_bin_array = self.center_bin_array(row_bin_array)
            self.bin_array.append(row_bin_array)

    def load(self):
        d.clear(update = False)
        for i in range(self.rows_to_show):
            self.d.load_row(self.bin_array[i], i)
    
    def show(self):
        self.load()
        self.d.update()

class ScrollText(TextEffect):
    def __init__(self, display, font,  text, sleeptime = 0.1):
        super().__init__(display, font, True, text)
        self.bin_array = self.text_to_bin()
        self.sleeptime = sleeptime
        ## Pad the message with empty space front and back
        for i in range(len(self.bin_array)):
            self.bin_array[i] = self.d.leds_on_row * '0' + self.bin_array[i]
            self.bin_array[i] += self.d.leds_on_row * '0'

    def show(self, row = 0, visual = False ):
        ## now roll through the data
        while len(self.bin_array[0]) >= self.d.leds_on_row:
            self.d.load_row(self.bin_array)
            self.d.update()
            for i in range(len(self.bin_array)):
                self.bin_array[i] = self.bin_array[i][1:]
            if visual:
                print(self.d)
            time.sleep(self.sleeptime)


if __name__ == '__main__':
    f = Font('ledFont')
    d = Display('10.23.5.143')

    StaticRow(d, f, '--Hanne--').show(1)
    effect = ScrollText(d, f, 'De kat krabt de krollen van de trap', sleeptime = 0.05)
    effect.show(visual = True)
print(d)
