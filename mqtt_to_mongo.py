import json
import paho.mqtt.client as mqtt
from pymongo import MongoClient
from datetime import datetime

# MongoDB setup
mongo_client = MongoClient("mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority")
db = mongo_client["zigbee"]
collection = db["sensor_data"]

# Callback when a message is received
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        payload["topic"] = msg.topic
        payload["timestamp"] = datetime.utcnow()
        collection.insert_one(payload)
        print(f"Inserted into MongoDB: {payload}")
    except Exception as e:
        print(f"Error: {e}")

# MQTT client setup
client = mqtt.Client()
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.subscribe("zigbee2mqtt/#")  # Listen to all Zigbee2MQTT topics

client.loop_forever()
