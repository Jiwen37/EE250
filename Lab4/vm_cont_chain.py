#Names: Jiwen Li (Jiwen37), Cynthia Liu (frawgmanman)
#GitHub Repo Name: Jiwen37/EE250

import paho.mqtt.client as mqtt
import time
from datetime import datetime
import socket



def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("cynthliu/ping")
    client.message_callback_add("cynthliu/ping", on_message_from_ping)

def on_message_from_ping(client, userdata, message):
    num_str = message.payload.decode()
    print("Custom callback  - Number: "+ num_str)

    num = int(num_str)
    num+=1
    time.sleep(1)
    client.publish("cynthliu/pong", str(num))
    print(f"Publishing number to pong: {num}")

if __name__ == '__main__':
    #create a client object
    client = mqtt.Client()

    client.on_connect = on_connect

    client.connect(host="172.20.10.4", port=1883, keepalive=60)


    client.loop_forever()
