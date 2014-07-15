import serial
import time
import socket

INC_IP=""
INC_PORT = 5000

incomming = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP

incomming.bind((INC_IP, INC_PORT))


ser = serial.Serial('/dev/ttyUSB0', 115200, timeout = 5)
time.sleep(3)

while True:
    try: 
        data, addr = incomming.recvfrom(189, socket.MSG_DONTWAIT)
        ser.write(data)
    except socket.error:
        pass
  ##  serialData = [i for i in range(189)]
  ##  serialData = bytearray(serialData)


