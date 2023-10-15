#!/usr/bin/python
import RPi.GPIO as GPIO
import picamera
import pygame
import paho.mqtt.client as mqtt
import ssl
import json
import time
import datetime
import _thread
from PIL import Image
from base64 import b64encode

def on_connect(client, userdata, flags, rc):
    print("Connected to AWS IoT: " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs='/home/pi/certs/Project/AmazonRootCA1.pem', certfile='/home/pi/certs/Project/device.pem.crt', keyfile='/home/pi/certs/Project/private.pem.key', tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("awujn3qqtf8mv-ats.iot.ap-southeast-2.amazonaws.com", 8883, 60)

AMP_CONTROL_PIN = 3
PIR_PIN = 7
armed = False
startTime = datetime.datetime.now()
endTime = datetime.datetime.now()


# initialize pygame
pygame.mixer.init()
audio_file_path = "/home/pi/Desktop/audio1.wav"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_PIN, GPIO.IN)  # Read output from PIR motion sensor
camera = picamera.PiCamera()
camera.resolution = (260, 195)
GPIO.setup(AMP_CONTROL_PIN, GPIO.OUT)         #Audio output pin

        
def publishData(txt):
    print(txt)
    
    client.publish("$aws/things/Door_Sensor/shadow/get", payload=json.dumps({"intruder": "Detected"}), qos=0, retain=False)
    
    def on_message(client, userdata, msg):
        global armed
        global startTime
        global endTime
        response = json.loads(msg.payload.decode())["state"]["reported"]
        print(response)
        if(response.get("Armed_Status") != None):
            armed = response["Armed_Status"]
            print("SET ARMED TO ", armed)
        if(response.get("Armed_Time") != None):
            timenow = datetime.datetime.now()
            year = timenow.year
            month = timenow.month
            day = timenow.day
            startTime = datetime.datetime.strptime(response["Armed_Time"]["Start"], "%H:%M")
            endTime = datetime.datetime.strptime(response["Armed_Time"]["End"], "%H:%M")
            startTime = startTime.replace(year=year, month=month, day=day)
            endTime = endTime.replace(year=year, month=month, day=day)
            print(startTime, " And ", endTime)
            print(endTime > datetime.datetime.now())
        
    client.subscribe([("$aws/things/Door_Sensor/shadow/+/accepted",0)])
    client.on_message = on_message
    time.sleep(0.5)
    
    client.publish("$aws/things/Door_Sensor/shadow/get", payload=json.dumps({"intruder": "Detected"}), qos=0, retain=False)

    
    while True:
        timeNow = datetime.datetime.now()
        i = GPIO.input(PIR_PIN)
        # When output from motion sensor is LOW
        if i == 0:
            #print("No intruders", i, armed)
            time.sleep(0.1)
            # Turn OFF Audio -temporary sanity measure good lord
            GPIO.output(AMP_CONTROL_PIN, GPIO.LOW)
        # When output from motion sensor is HIGH
        elif i == 1 and armed == True :
            if((startTime < endTime and startTime < timeNow and endTime > timeNow) or (startTime > endTime and (startTime < timeNow or endTime > timeNow))):
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
                with open("intruder.jpg", "rb") as f:
                    b64img = b64encode(f.read())
                f.close()
                time.sleep(0.1)
                
                timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                
                client.publish("intruder/detected", payload=json.dumps({"intruder": "Detected", "Timestamp": timestamp, "image": b64img.decode("utf-8")}), qos=0, retain=False)
            



 
_thread.start_new_thread(publishData,("Spin-up new Thread...",))
client.loop_forever()
