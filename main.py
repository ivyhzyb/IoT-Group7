#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import picamera

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)  # Read output from PIR motion sensor
camera = picamera.PiCamera()
# GPIO.setup(3, GPIO.OUT)         #Audio output pin

while True:
    i = GPIO.input(7)
    if i == 0:  # When output from motion sensor is LOW
        print("No intruders", i)
        #		GPIO.output(3, 0)  #Turn OFF Audio
        time.sleep(0.1)
    elif i == 1:  # When output from motion sensor is HIGH
        print("Intruder detected", i)
        #		GPIO.output(3, 1)  #Turn ON Audio
        camera.capture("intruder.jpg")
        time.sleep(0.1)
