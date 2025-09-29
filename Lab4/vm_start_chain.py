#Names: Jiwen Li (Jiwen37), Cynthia Liu (frawgmanman)
#GitHub Repo Name: Jiwen37/EE250

import paho.mqtt.client as mqtt
import time
import socket

num = 0

def on_connect(client,userdata,flags,rc):
    print("Connected to server with results code "+str(rc))
    client.subscribe("cynthliu/pong")

    client.message_callback_add("cynthliu/pong", on_message_from_pong)

    client.publish("cynthliu/ping", str(num))
    print("Publishing initial number to ping: " + str(num))

def on_message_from_pong(client, userdata, message):
    new_num = message.payload.decode()
    print("Received Number: " + new_num)

    num = int(new_num)
    num += 1
    time.sleep(1)
    client.publish("cynthliu/ping", str(num))
    print(f"Publishing number to ping: {num}")


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(host="172.20.10.4", port=1883, keepalive=60) #host?

    client.loop_forever()
