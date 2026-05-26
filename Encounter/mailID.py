import uuid
import datetime

def generate_email_uuid():
    # Create a time-based UUID + timestamp for extra uniqueness
    unique_id = uuid.uuid4()  # Random UUID
    timestamp = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    email_uuid = f"EmailUUID-{timestamp}-{unique_id}"
    return email_uuid

if __name__ == "__main__":
    uid = generate_email_uuid()
    print(f"Generated EmailUUID: {uid}")
