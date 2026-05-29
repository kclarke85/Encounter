"""
iothub_to_mongo.py — Sentinel Hive Mind Bridge
Encounter Engineering · Patent Pending

Reads telemetry from Azure IoT Hub (via Event Hub protocol)
and writes to MongoDB sentinel_telemetry collection.

Run: python iothub_to_mongo.py

Requires (add to requirements.txt):
    azure-eventhub==5.11.7
"""

import asyncio
import json
import os
from datetime import datetime, timezone

from azure.eventhub.aio import EventHubConsumerClient
from pymongo import MongoClient, DESCENDING
from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
# Paste your IoT Hub → Built-in endpoints → Event Hub-compatible connection string
# Azure Portal → Encounter IoT Hub → Built-in endpoints → copy "Event Hub-compatible endpoint"
# Then append ;EntityPath=encounter  (your hub path from earlier)
EVENTHUB_CONNECTION_STR = os.getenv(
    "IOTHUB_EVENTHUB_CONNECTION_STR",
    "Endpoint=sb://iothub-ns-encounter-71396801-8663749ae0.servicebus.windows.net/;"
    "SharedAccessKeyName=service;"
    "SharedAccessKey=L1u0rfdeWpHqyTrM5FbTWC/L8uyePRgh6AIoTBnMUYw=;"
    "EntityPath=encounter"
)
EVENTHUB_NAME       = "encounter"          # path from az iot hub show
CONSUMER_GROUP      = "sentinel-consumer"  # created earlier

MONGO_URI           = os.getenv("MONGO_URI")
DB_NAME             = "encounter_db"
COLLECTION_NAME     = "sentinel_telemetry"

# ── MongoDB setup ─────────────────────────────────────────────────────────────
mongo_client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db           = mongo_client[DB_NAME]
telemetry    = db[COLLECTION_NAME]

# TTL index: auto-delete docs older than 30 days (keeps collection lean)
telemetry.create_index("receivedAt", expireAfterSeconds=60 * 60 * 24 * 30)
# Index on deviceId for fast portal queries
telemetry.create_index([("deviceId", 1), ("receivedAt", DESCENDING)])

print(f"[Sentinel Bridge] Connected to MongoDB → {DB_NAME}.{COLLECTION_NAME}")
print(f"[Sentinel Bridge] Listening on IoT Hub consumer group: {CONSUMER_GROUP}")


# ── Event handler ─────────────────────────────────────────────────────────────
async def on_event(partition_context, event):
    try:
        raw      = event.body_as_str(encoding="UTF-8")
        payload  = json.loads(raw)

        # Stamp with server-side receive time
        payload["receivedAt"] = datetime.now(timezone.utc)

        # Upsert: keep one "latest" doc per device + full history
        telemetry.insert_one(payload)

        classification = payload.get("triage", {}).get("classification", "UNKNOWN")
        score          = payload.get("triage", {}).get("priorityScore", 0)
        device_id      = payload.get("deviceId", "?")

        print(f"[TX] {device_id} → {classification} (score {score})")

    except json.JSONDecodeError:
        print(f"[WARN] Non-JSON message received, skipping")
    except Exception as e:
        print(f"[ERROR] {e}")

    await partition_context.update_checkpoint(event)


# ── Main loop ─────────────────────────────────────────────────────────────────
async def main():
    client = EventHubConsumerClient.from_connection_string(
        conn_str=EVENTHUB_CONNECTION_STR,
        consumer_group=CONSUMER_GROUP,
        eventhub_name=EVENTHUB_NAME,
    )
    print("[Sentinel Bridge] Running. Ctrl+C to stop.\n")
    async with client:
        await client.receive(
            on_event=on_event,
            starting_position="-1",  # "-1" = only new messages; "@latest" also works
        )


if __name__ == "__main__":
    asyncio.run(main())
