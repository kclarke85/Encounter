from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient, DESCENDING
from dotenv import load_dotenv
from datetime import datetime
import os
import json

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True,
    serverSelectionTimeoutMS=5000
)
db = client["encounter_db"]
collection       = db["test"]
devices_col      = db["devices"]
alerts_col       = db["alerts"]
network_col      = db["network"]
stakeholders_col = db["stakeholders"]
telemetry_col    = db["sentinel_telemetry"]


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


# Sentinel Hive Mind telemetry routes

@app.get("/sentinel/telemetry/latest")
def get_latest_telemetry():
    pipeline = [
        {"$sort": {"receivedAt": -1}},
        {"$group": {"_id": "$deviceId", "latest": {"$first": "$$ROOT"}}},
        {"$replaceRoot": {"newRoot": "$latest"}},
        {"$project": {"_id": 0}}
    ]
    results = list(telemetry_col.aggregate(pipeline))
    return {"ok": True, "count": len(results), "devices": results}


@app.get("/sentinel/telemetry/{device_id}")
def get_device_telemetry(device_id: str, limit: int = 50):
    docs = list(
        telemetry_col
        .find({"deviceId": device_id}, {"_id": 0})
        .sort("receivedAt", DESCENDING)
        .limit(limit)
    )
    if not docs:
        raise HTTPException(status_code=404, detail=f"No telemetry for {device_id}")
    return {"ok": True, "deviceId": device_id, "readings": docs}


@app.post("/sentinel/ingest")
def ingest_telemetry(data: dict):
    data["receivedAt"] = datetime.utcnow().isoformat()
    if "_id" in data:
        del data["_id"]
    telemetry_col.insert_one(data)
    return {"ok": True, "message": "Telemetry ingested"}