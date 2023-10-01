#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import picamera
import pygame

AMP_CONTROL_PIN = 3
PIR_PIN = 7
audio_file_path = "/home/pi/Desktop/audio1.wav"

def setup():
    """Initial setup for GPIO and other components."""
    pygame.mixer.init()
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIR_PIN, GPIO.IN)  # Read output from PIR motion sensor
    GPIO.setup(AMP_CONTROL_PIN, GPIO.OUT)   # Audio output pin
    pygame.mixer.music.load(audio_file_path)  # Load audio file once

def play_audio():
    """Play the audio file."""
    GPIO.output(AMP_CONTROL_PIN, GPIO.HIGH)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass
    GPIO.output(AMP_CONTROL_PIN, GPIO.LOW)

def capture_image(camera, image_num):
    """Capture an image with a unique filename."""
    camera.capture(f"intruder_{image_num}.jpg")

def main():
    """Main loop for motion detection."""
    camera = picamera.PiCamera()
    image_num = 0

    while True:
        i = GPIO.input(PIR_PIN)
        # When output from motion sensor is LOW
        if i == 0:
            print("No intruders", i)
            time.sleep(0.1)
        # When output from motion sensor is HIGH
        elif i == 1:
            print("Intruder detected", i)
            play_audio()
            image_num += 1
            capture_image(camera, image_num)
            time.sleep(0.1)

if __name__ == "__main__":
    setup()
    main()
