#!/usr/bin/env python3
import json
import sys
import os.path
import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

scale_id_file = 'scale_id'

#publish.single("testTopic", "Hello from rz02!", hostname="mqtt.hivespeak.tk")

def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    # client.subscribe("scale/zero", 1)  # Subscribe to the topic “digitest/test1”, receive any messages published on it
    s1 = "scale/" + scale_id + "/zero"
    s2 = "scale/" + scale_id + "/get_raw"
    print(s1,s2)
    client.subscribe([(s1, 1),(s2,1)])

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
	print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
	try:
		GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
		# Create an object hx which represents your real hx711 chip
		# Required input parameters are only 'dout_pin' and 'pd_sck_pin'
		hx = HX711(dout_pin=21, pd_sck_pin=20)

		reading = hx.get_raw_data_mean()
		if reading:  # always check if you get correct value or only False
			# now the value is close to 0
			print('Data subtracted by offset but still not converted to units:',
			reading)
		else:
			print('invalid data', reading)

		print('zero')
		payload={
			"cmd":msg.topic,
			"data": reading
			}
		result = json.dumps(payload)
		print(result)
		client.publish("scale/send_raw",result)

	except (KeyboardInterrupt, SystemExit, TypeError, ValueError):
		print('Bye :)') 
	finally:
		GPIO.cleanup()


if not os.path.exists(scale_id_file):
	print('Please define the scale ID in the file named scale_id')
	exit(1)

scale_id = ''
with open(scale_id_file, "r") as id_f:
	data = json.load(id_f)
	print(data)
	scale_id = data["scale_id"]
	print(scale_id)


client = mqtt.Client("digi_mqtt_test")  # Create instance of client with client ID “digi_mqtt_test”
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
client.on_publish = on_publish
client.connect("mqtt.hivespeak.tk", 1883, 60)  # Connect to (broker, port, keepalive-time)
# client.connect('127.0.0.1', 17300)
client.loop_forever()  # Start networking daemon

 
