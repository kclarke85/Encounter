from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os
import json

load_dotenv()

app = FastAPI()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["encounter_db"]

collection       = db["test"]
devices_col      = db["devices"]
alerts_col       = db["alerts"]
network_col      = db["network"]
stakeholders_col = db["stakeholders"]

@app.get("/")
def read_root():
    return {"status": "Encounter API running"}

@app.post("/add")
def add_item(data: dict):
    collection.insert_one(data)
    return {"message": "Data inserted"}

@app.get("/all")
def get_all():
    return list(collection.find({}, {"_id": 0}))

@app.get("/devices")
def get_devices():
    return list(devices_col.find({}, {"_id": 0}))

@app.get("/devices/{device_id}")
def get_device(device_id: str):
    device = devices_col.find_one({"id": device_id}, {"_id": 0})
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@app.get("/alerts")
def get_alerts():
    return list(alerts_col.find({"status": "active"}, {"_id": 0}))

@app.get("/network")
def get_network():
    return network_col.find_one({}, {"_id": 0})

@app.get("/stakeholders")
def get_stakeholders():
    return list(stakeholders_col.find({}, {"_id": 0}))

@app.get("/api/sentinel-data")
def get_sentinel_data():
    return {
        "devices":      list(devices_col.find({}, {"_id": 0})),
        "alerts":       list(alerts_col.find({}, {"_id": 0})),
        "network":      network_col.find_one({}, {"_id": 0}),
        "stakeholders": list(stakeholders_col.find({}, {"_id": 0}))
    }

@app.post("/ingest")
def ingest_reading(data: dict):
    data["timestamp"] = datetime.utcnow().isoformat()
    db["readings"].insert_one(data)
    return {"message": "Reading stored", "device": data.get("device_id")}

@app.post("/seed")
def seed_data():
    with open("sentinel-mock-data.json", encoding="utf-8") as f:
        data = json.load(f)
    devices_col.drop()
    alerts_col.drop()
    network_col.drop()
    stakeholders_col.drop()
    devices_col.insert_many(data["devices"])
    alerts_col.insert_many(data["alerts"])
    stakeholders_col.insert_many(data["stakeholders"])
    network_col.insert_one(data["network"])
    return {"message": f"Seeded {len(data['devices'])} devices, {len(data['alerts'])} alerts"}