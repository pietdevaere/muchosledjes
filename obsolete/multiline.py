import RPi.GPIO as GPIO
import spidev
import time

RCK = 18    ## pin for row clock
SRCK = 17     ## pin to show loaded data
SEROUT2 = 4  ## pin for row serial data

spi = spidev.SpiDev()
spi.open(0, 1)
spi.max_speed_hz = int(1e6)
spi.mode = 0

## set up the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SRCK, GPIO.OUT)
GPIO.setup(RCK, GPIO.OUT)
GPIO.setup(SEROUT2, GPIO.OUT)

GPIO.output(SRCK, GPIO.LOW)
GPIO.output(RCK, GPIO.LOW)
GPIO.output(SEROUT2, GPIO.HIGH)

displayData = [[0x01]*27, [0x02]*27, [0x04]*27, [0x08]*27,  [0x10]*27,  [0x20]*27, [0x40]*27] 

signalDelay = 0.000001
displayTime = 0.001

def first_row():
    GPIO.output(SEROUT2, GPIO.LOW)
    time.sleep(signalDelay)
    GPIO.output(SRCK, GPIO.HIGH)
    time.sleep(signalDelay)
    GPIO.output(SRCK, GPIO.LOW)
    GPIO.output(SEROUT2, GPIO.HIGH)

def next_row():
    GPIO.output(SRCK, GPIO.HIGH)
    time.sleep(signalDelay)
    GPIO.output(SRCK, GPIO.LOW)

def show_data():
    GPIO.output(RCK, GPIO.HIGH)
    time.sleep(signalDelay)
    GPIO.output(RCK, GPIO.LOW)



while True:
#for i in range(10000):
    first_row()
    for i in range(7):
        mem = spi.writebytes(displayData[i])
        if i != 0:
            next_row()
        time.sleep(signalDelay)
        show_data()
        time.sleep(displayTime)

try:
    input()
except:
    pass

spi.close()
GPIO.cleanup()



