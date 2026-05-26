import os
import time
import logging
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load environment variables
load_dotenv()
logging.basicConfig(level=logging.INFO)

# Config
APPLICANT_NAME = os.getenv("APPLICANT_NAME")
APPLICANT_EMAIL = os.getenv("APPLICANT_EMAIL")
RESUME_PATH = os.getenv("RESUME_PATH")

def apply_to_job(job):
    logging.info(f"🚀 Applying to: {job['title']} at {job['company']}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto(job["apply_url"], timeout=30000)

            # Fill out the form (adjust selectors as needed)
            page.fill('input[name="name"]', APPLICANT_NAME)
            page.fill('input[name="email"]', APPLICANT_EMAIL)
            page.set_input_files('input[type="file"]', RESUME_PATH)
            page.click('button[type="submit"]')

            logging.info("✅ Application submitted successfully")
            browser.close()
    except Exception as e:
        logging.error(f"❌ Failed to apply: {e}")

# Example job list
jobs = [
    {
        "title": "QA Engineer",
        "company": "TechCorp",
        "apply_url": "https://example.com/apply/qa-engineer"
    },
    # Add more jobs here
]

# Apply to each job
for job in jobs:
    apply_to_job(job)
