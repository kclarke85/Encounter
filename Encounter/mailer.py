import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
import time

# === CONFIG ===

CSV_FILE = 'test.csv'

# --- If loading from files ---
# SUBJECT_FILE = 'subject.txt'
# BODY_FILE = 'body.html'

# --- Or direct text ---
EMAIL_SUBJECT = 'NYC LL 144: Your Annual AEDT Audit simplified'

EMAIL_BODY = """
<html>
  <body>
    <p>Hello,</p>
    <p>Here’s what you need to know about your NYC Local Law 144 compliance this year.</p>
    <p>Check out <a href="https://www.encounterengineering.com">Encounter Engineering</a> for more details.</p>
    <p>Best regards,<br>K.Clarke</p>
  </body>
</html>
"""

ATTACHMENT_PATH = 'July Newsletter 2025.pdf'

GMAIL_USER = 'k.clarke@encounter-engineering.com'
GMAIL_PASSWORD = 'Tuesday19@@@@'

BCC_EMAIL = 'kclarke85@hotmail.com'

# Schedule when to start
SCHEDULE_TIME = '2025-07-03 21:00'  # YYYY-MM-DD HH:MM

BATCH_SIZE = 8
WAIT_TIME = 3600  # seconds (1 hour)

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# === LOAD CSV ===

df = pd.read_csv(CSV_FILE)
emails = df['email'].tolist()

# === If loading from files ===
# with open(SUBJECT_FILE, 'r') as f:
#     EMAIL_SUBJECT = f.read().strip()
# with open(BODY_FILE, 'r') as f:
#     EMAIL_BODY = f.read()

# === WAIT UNTIL SCHEDULE ===

print(f"Scheduled to start at: {SCHEDULE_TIME}")
start_time = datetime.strptime(SCHEDULE_TIME, '%Y-%m-%d %H:%M')

while datetime.now() < start_time:
    print(f"Waiting... Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    time.sleep(30)

print("Starting email sending process...")

# === SEND ===

current_index = 0

while True:
    print("Starting new batch...")
    for i in range(BATCH_SIZE):
        recipient = emails[current_index]

        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = recipient
        msg['Bcc'] = BCC_EMAIL
        msg['Subject'] = EMAIL_SUBJECT

        # Attach HTML body
        msg.attach(MIMEText(EMAIL_BODY, 'html'))

        # Attach file
        with open(ATTACHMENT_PATH, 'rb') as f:
            part = MIMEApplication(f.read(), Name=ATTACHMENT_PATH)
        part['Content-Disposition'] = f'attachment; filename="{ATTACHMENT_PATH}"'
        msg.attach(part)

        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            print(f"✅ Sent to: {recipient}")
        except Exception as e:
            print(f"❌ Failed to send to {recipient}: {e}")

        current_index += 1
        if current_index >= len(emails):
            current_index = 0

    print(f"Batch complete. Next batch in {WAIT_TIME/60} minutes...")
    time.sleep(WAIT_TIME)



