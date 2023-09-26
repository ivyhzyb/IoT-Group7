#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import picamera
import pygame

AMP_CONTROL_PIN = 3
PIR_PIN = 7

# initialize pygame
pygame.mixer.init()
audio_file_path = "/home/pi/Desktop/audio1.wav"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_PIN, GPIO.IN)  # Read output from PIR motion sensor
camera = picamera.PiCamera()
GPIO.setup(AMP_CONTROL_PIN, GPIO.OUT)   #Audio output pin


while True:
    i = GPIO.input(PIR_PIN)
    # When output from motion sensor is LOW
    if i == 0:
        print("No intruders", i)
        time.sleep(0.1)
    # When output from motion sensor is HIGH
    elif i == 1:
        print("Intruder detected", i)
        # Turn ON Audio
        GPIO.output(AMP_CONTROL_PIN, GPIO.HIGH)
        pygame.mixer.music.load(audio_file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pass
        # Turn OFF Audio
        GPIO.output(AMP_CONTROL_PIN, GPIO.LOW)
        # Take picture
        camera.capture("intruder.jpg")
        time.sleep(0.1)
