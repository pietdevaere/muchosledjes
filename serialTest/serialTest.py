import serial

serialData = [i for i in range(189)]


serialData = bytearray(serialData)
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout = 5)
while True:
    raw_input()
    ser.write(serialData)
    echo = ser.read(189)
    for char in echo:
        print(ord(char)),
