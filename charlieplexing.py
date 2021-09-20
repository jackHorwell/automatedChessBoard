import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

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


# Function to flash all LEDs 3 times
def allFlash():
    for i in range(3):
        for j in range(1000):
            for k in range(17):
                turnOn(k)

        turnOn(0)
        time.sleep(0.2)


# Function to turn on each LED one at a time in order
# Speed depends on the input
def slide(speed):
    if speed == "fast":
        delay = 0.05
    elif speed == "slow":
        delay = 0.5
        
    for i in range(1, 17):
        turnOn(i)
        time.sleep(delay)

# Function to have LED "bounce" back and forth
def bounce():
    for i in range(1, 17):
        for j in range(2000):
            turnOn(i)
            turnOn(17 - i)
