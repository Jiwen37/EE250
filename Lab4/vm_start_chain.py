import paho.mqtt.client as mqtt
import time
import socket

def on_connect(client,userdata,flags,rc):
    print("Connected to server with results code "+str(rc))
    client.subscribe("cynthliu/pong")

    client.message_callback_add("cynthliu/pong", on_message_from_pong)
def on_message(client, userdata, msg):
    print("default callback")
def on_message_from_pong(client, userdata, message):
    print(message.payload.decode())

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="172.20.10.4", port=1883, keepalive=60) #host?

    client.loop_start()
    time.sleep(1)

    while True:
        client.publish("cynthliu/ping", f"ping")
        print(f"published ping\n")
        time.sleep(1)
