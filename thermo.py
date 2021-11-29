#!/usr/bin/env python3

#import sys
import os
#import time
import requests
import Adafruit_DHT
import dht11
import RPi.GPIO as GPIO

from params import *


f = open(".httoken", "r")
auth_token = f.read()
request_url = server_url + auth_token

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


# SENSOR: Send temperature and humidity
if enable_sensor == 1:
    print('Send temperature and humidity')

    humidity, temperature = Adafruit_DHT.read_retry(sensor_model, sensor_pin)

    print('Temperature: ' + str(temperature))
    print('Humidity: ' + str(humidity))

    if humidity is not None and temperature is not None:
        request_url += '&temperature=' + str(temperature)
        request_url += '&humidity=' + str(humidity)
    else:
        print('Failed to get sensor reading')

# using szazo library gives decimal precision in DHT11
if enable_sensor == 2:
    print('Send temperature and humidity')
    instance = dht11.DHT11(pin = sensor_pin)
    result = instance.read()

    print('Temperature: ' + str(result.temperature))
    print('Humidity: ' + str(result.humidity))

    if result.is_valid():
        request_url += '&temperature=' + str(result.temperature)
        request_url += '&humidity=' + str(result.humidity)
    else:
        print("ERROR: %d" % result.error_code)


# PRESENCE: Ping devices IP
presence = '0'
if enable_presence == 1:
    print('Ping devices IP:')
    for ip in ips:
        print('Ping ' + ip)
        exit_code = os.system(f"ping -c 1 -w2 {ip} > /dev/null 2>&1")
        print(exit_code)
        if exit_code == 0: # if exit_code is 0 then the ip was found!
            presence = '1'
    request_url += '&presence=' + presence


# MAKE REQUEST
if enable_test == 0:
    print('REQUEST ' + request_url)
    r = requests.get(request_url)


# RELAY: on/off switch
if enable_relay == 1:
    print('Relay ' + str(relay_channel) + ':')
    # initialize GPIO
    #GPIO.setup(relay_channel, GPIO.OUT)
    os.system("gpio -g mode 24 out")

    if r.text == 'on':
        print('Status: ON')
        print('RELAY: ON')
        os.system("gpio -g write 24 0")

    elif r.text == 'off':
        # this relay might need to be turned on then off for it to work
        print('Status: off')
        print('RELAY: off')
        os.system("gpio -g write 24 1")
        # time.sleep(0.5)
        # os.system("gpio -g write 24 0")

    GPIO.cleanup()


print('Response: ' + r.text)
