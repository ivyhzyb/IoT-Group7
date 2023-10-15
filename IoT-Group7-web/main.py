#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import picamera

AMP_CONTROL_PIN = 3
PIR_PIN = 7

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_PIN, GPIO.IN)  # Read output from PIR motion sensor
camera = picamera.PiCamera()
GPIO.setup(AMP_CONTROL_PIN, GPIO.OUT)         #Audio output pin

while True:
    i = GPIO.input(PIR_PIN)
    if i == 0:  # When output from motion sensor is LOW
        print("No intruders", i)
        GPIO.output(AMP_CONTROL_PIN, GPIO.LOW)  #Turn OFF Audio
        time.sleep(0.1)
    elif i == 1:  # When output from motion sensor is HIGH
        print("Intruder detected", i)
        GPIO.output(AMP_CONTROL_PIN, GPIO.HIGH)  #Turn ON Audio
        camera.capture("intruder.jpg")
        time.sleep(0.1)
