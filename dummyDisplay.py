#!/usr/bin/python3
import socket

## some information about the display
chars_on_row = 18
chars_on_disp = 36
leds_on_line = 216
leds_on_row = leds_on_line//2
bytes_on_line = 27
lines = 7
rows = 2
total_bytes = bytes_on_line*lines

## Set up the socket
ip = ""
port = 5000
receiving_socket = socket.socket(socket.AF_INET, # internet
        socket.SOCK_DGRAM) # udp
receiving_socket.bind((ip, port))

while True:
## Receive some data
    try:
        data, addr = receiving_socket.recvfrom(1024)
    except socket.error:
        continue
    else:
        # convert it to a binary string
        received_string = ""
        for byte in data:
            char_string = "{1:0>8b}".format(received_string, byte)
            received_string += char_string
            display_string = received_string.replace('1', chr(9608)).replace('0', 'x')
        
        # replace 1 by filled, and 0 by space
        received_string 
        
        # now clip in in to lines for the display
        display = [ [] for i in range(lines*rows)]
        
        for line in range(lines):
            start_index = line * leds_on_line
            middle_index = start_index + leds_on_row
            stop_index = (line + 1) * leds_on_line
            display[line] = display_string[start_index:middle_index]
            display[lines + line] = display_string[middle_index : stop_index]
        
        for i in range(lines*rows):
            print(display[i])
            if i == lines - 1:
                print('-'*leds_on_row)
                
        print('\n'*5)
        
        
       



