import paho.mqtt.client as mqtt
import threading
import time
from func.Uid_check import Uid_check
from func.Rental import Rental
from func.Return import Return
from func.Overdue_check import check_overdue_users

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT with result code", rc)
    client.subscribe("uid/check")
    client.subscribe("umbrella/rental")
    client.subscribe("umbrella/return")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"Received message on topic {topic}: {payload}")

    if topic == "uid/check":
        Uid_check(payload, client)
    elif topic == "umbrella/rental":
        Rental(payload, client)
    elif topic == "umbrella/return":
        Return(payload, client)
        
def overdue_loop():
    while True:
        check_overdue_users()
        time.sleep(60)  # 60초마다 실행


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
threading.Thread(target=overdue_loop, daemon=True).start()
client.loop_forever()
