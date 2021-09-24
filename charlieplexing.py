import time

from enum import Enum

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

numberOfLeds = 16

class Speed(Enum):
    fast = 0.05
    medium = 0.25
    slow = 0.5
    

# Function that takes the LED number you want to turn on and
# turns on/off the corresponding pins
def turnOn(led):
    # Array that stores which pins should be high or low
    # for the charlieplex to work, first number indicates
    # pin to be high and second low. Omits pins that should
    # be inputs.
    # Zero index will reset all pins and turn off any LEDs
    charlieplexingPins = [
        [6, 26], # Unused configuration, will not light anything up
        [6, 5],
        [13, 6],
        [19, 13],
        [26, 19],
        [5, 6],
        [6, 13],
        [13, 19],
        [19, 26],
        [13, 5],
        [26, 13],
        [5, 13],
        [13, 26],
        [26, 5],
        [5, 26],
        [19, 6],
        [6, 19]
    ]

    # Sets all pins to be inputs (essentially disconnected)
    # Added benefit of reseting any previously on LEDs to be off
    GPIO.setup(5, GPIO.IN)
    GPIO.setup(6, GPIO.IN)
    GPIO.setup(13, GPIO.IN)
    GPIO.setup(19, GPIO.IN)
    GPIO.setup(26, GPIO.IN)

    # Resets necessary pins to be outputs and set to HIGH or LOW
    GPIO.setup(charlieplexingPins[led][0], GPIO.OUT)
    GPIO.setup(charlieplexingPins[led][1], GPIO.OUT)
    GPIO.output(charlieplexingPins[led][0], GPIO.HIGH)
    GPIO.output(charlieplexingPins[led][1], GPIO.LOW)


# Function to turn off all LEDs
def turnAllOff():
    turnOn(0)


# Function to flash all LEDs 3 times
def allFlash(numberOfFlashes = 3):
    # Number of times the program will turn on each LED
    # The higher the number, the longer the LEDs will be on
    ledCycle = 500
    # Sleep time on seconds, 0.1s = 100ms
    sleepTimeSeconds = 0.1
    
    for _ in range(numberOfFlashes):
        for _ in range(ledCycle):
            for ledId in range(1, numberOfLeds + 1):
                turnOn(ledId)

        turnAllOff()
        time.sleep(sleepTimeSeconds)


# Function to turn on each LED one at a time in order
# Speed depends on the input
def slide(speedString):
    # Delay is in milliseconds
    delay = Speed[speedString].value
        
    for ledId in range(1, numberOfLeds + 1):
        turnOn(ledId)
        time.sleep(delay)

# Function to have LED "bounce" back and forth
def bounce():
    # Number of times the program will turn on each LED
    # The higher the number, the longer the LEDs will be on
    ledCycle = 2000
    
    for ledId in range(1, numberOfLeds + 1):
        xLedId = ledId
        yLedId = numberOfLeds + 1 - ledId
        
        for _ in range(ledCycle):
            turnOn(xLedId)
            turnOn(yLedId)
