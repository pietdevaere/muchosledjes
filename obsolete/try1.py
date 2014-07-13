import RPi.GPIO as GPIO
import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 1)
spi.max_speed_hz = int(1e4)
spi.mode = 0


GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

GPIO.output(17, GPIO.LOW)
GPIO.output(18, GPIO.LOW)

try:
    resp = spi.xfer2([0x01]*27)
    spi.close()
    print(resp)
except:
    spi.close()
    print("writing to spi bus failed")

for i in range (10):
    GPIO.output(17, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(17, GPIO.LOW)
    time.sleep(0.00001)


GPIO.output(18, GPIO.HIGH)
time.sleep(0.001)
GPIO.output(18, GPIO.LOW)
time.sleep(0.001)

try: 
    input()
except:
    pass

spi.close()
GPIO.cleanup()
