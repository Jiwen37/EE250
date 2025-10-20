import sys
sys.path.append('~/Dexter/GrovePi/Software/Python')
import time
import grovepi
import grove_rgb_lcd as lcd

# Grove Ultrasonic Ranger connectd to digital port 2
ultrasonic_ranger = 2
# potentiometer connected to analog port A0 as input
potentiometer = 0
grovepi.pinMode(potentiometer,"INPUT")

# clear lcd screen  before starting main loop
lcd.setText("")

while True:
  try:
    # TODO:read distance value from Ultrasonic Ranger and print distance on LCD
    distance = grovepi.ultrasonicRead(ultrasonic_ranger)
    
    #lcd.setText("\n" + str(distance))

    # TODO: read threshold from potentiometer
    threshold = grovepi.analogRead(potentiometer)
    
    # TODO: format LCD text according to threshhold
    object_present = 0
    if distance < threshold:
      object_present = 1

    if object_present:
      lcd.setText_norefresh(str(threshold)+" OBJ PRES" + "\n" + str(distance))
      lcd.setRGB(255, 0, 0)
    else:
      lcd.setText_norefresh(str(threshold) + "\n" + str(distance))
      lcd.setRGB(0, 255, 0)
  
  except IOError:
    print("Error")
