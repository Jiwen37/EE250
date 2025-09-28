import paho.mqtt.client as mqtt
import time
import socket

num = -1

def on_connect(client,userdata,flags,rc):
    print("Connected to server with results code "+str(rc))
    client.subscribe("cynthliu/ping")

    client.message_callback_add("cynthliu/ping", on_message_from_pong)
def on_message_from_pong(client, userdata, message):
    new_num = int(message_payload.decode())
    if(num!=new_num):
        num = new_num + 1
    print(message.payload.decode())

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(host="172.20.10.4", port=1883, keepalive=60) #host?

    client.loop_start()
    time.sleep(1)

    while True:

        client.publish("cynthliu/pong", f"{num}")
        print(f"published pong\n")
        time.sleep(1)