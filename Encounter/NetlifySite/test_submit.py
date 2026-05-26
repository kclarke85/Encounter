import random
import secrets
import requests
from datetime import datetime

# Target endpoint for your live Netlify site
NETLIFY_ENDPOINT = "https://encounterengineering.org/.netlify/functions/mongo"


def generate_mock_user():
    """Generates a random user payload wrapped in the structure the API expects."""
    random_account_id = secrets.token_hex(12)

    first_names = ["Druzell", "Alex", "Jordan", "Taylor", "Morgan"]
    last_names = ["Wlater", "Smith", "Davis", "Jones", "Brown"]
    organizations = ["WHO", "CDC", "Red Cross", "Encounter Eng", "UNICEF"]
    roles = ["Hospital / Clinic", "Field Responder", "Logistics Liaison", "Data Analyst"]

    selected_first = random.choice(first_names)
    selected_last = random.choice(last_names)

    # The payload structure that matches your API's expected format
    payload = {
        "action": "insert",
        "user_data": {
            "_id": random_account_id,
            "first_name": selected_first,
            "last_name": selected_last,
            "organization": random.choice(organizations),
            "email": f"{selected_first.lower()}.{selected_last.lower()}@example.org",
            "role": random.choice(roles),
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
    }
    return payload


def submit_form():
    payload = generate_mock_user()

    print("--- Submitting Payload to API ---")
    print(f"Action: {payload['action']}")
    print(f"User ID: {payload['user_data']['_id']}")
    print("--------------------------")

    try:
        response = requests.post(
            NETLIFY_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        print(f"Status Code Returned: {response.status_code}")
        print(f"Server Response Body: {response.text}")

        if response.status_code in [200, 201]:
            print("\n✅ Success! The data was accepted by the server.")
        else:
            print(f"\n❌ Submission failed with status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Network or Connection breakdown: {e}")


if __name__ == "__main__":
    submit_form()