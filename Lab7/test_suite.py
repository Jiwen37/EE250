import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

#using physical pin 11 to blink an LED
GPIO.setmode(GPIO.BOARD)
chan_list = [11]
GPIO.setup(chan_list, GPIO.OUT)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# by taking readings and printing them out, find
# appropriate threshold levels and set them 
# accordingly. Then, use them to determine
# when it is light or dark, quiet or loud.
lux_threshold=500  # change this value
sound_threshold=400 # change this value


while True: 
  time.sleep(0.5) 

  #Following commands control the state of the output
  #GPIO.output(pin, GPIO.HIGH)
  #GPIO.output(pin, GPIO.LOW)

  # get reading from adc 
  # mcp.read_adc(adc_channel)

  #blink LED 5 times interval 500 ms
  for i in range (5):
    GPIO.output(11, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(11, GPIO.LOW)
    time.sleep(0.5)

  #read output of light sensor every 100 ms for 5 seconds, print value + bright/dark
  total_time=0
  while total_time<5:
    light = mcp.read_adc(0)
    if light<lux_threshold:
      print(light, "dark")
    else:
      print(light, "bright")

    total_time+=0.1
    time.sleep(0.1)

  #blink LED 4 times interval 200 ms
  for i in range (4):
    GPIO.output(11, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(11, GPIO.LOW)
    time.sleep(0.2)

  #read output of sound sensor every 100 ms for 5 seoncds, print value, turn LED on for 100 ms if loud
  total_time = 0
  while total_time<5:
    sound = mcp.read_adc(1)
    print(sound)
    if sound>sound_threshold:
      GPIO.output(11, GPIO.HIGH)

    time.sleep(0.1)
    GPIO.output(11, GPIO.LOW)
    total_time+=0.1
