import requests
import urllib.parse
import csv
import re
import sys
import time

# === CONFIG ===
API_KEY = "AIzaSyDU4lalYx2H4G23CT233Yq_JsEd0Ox3rd0"  # Replace with your real API key
CX = "510c555d9fcec4974"                             # Replace with your real CSE ID

# === Roles/Titles you want to search for ===
roles = [
    "Chief People Officer"
]

# === Constants ===
RESULTS_PER_PAGE = 10  # Google Custom Search limit
PAGES = 4             # How many pages you want to fetch per role
OUTPUT_FILE = "linkedin_workforce_management.csv"

# === Email Extractor ===
def extract_email(text):
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group(0) if match else ""

# === Safe request with exponential backoff ===
def safe_request(url, max_retries=5):
    wait_time = 5
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                print(f"Rate limited by API. Waiting {wait_time} seconds before retry {attempt + 1}/{max_retries}...")
                time.sleep(wait_time)
                wait_time *= 2  # Exponential backoff
            else:
                print(f"HTTP error: {e}")
                print("Response content:", response.text)
                sys.exit(1)
    print("Max retries exceeded due to rate limiting. Exiting.")
    sys.exit(1)

# === Main ===
def main():
    unique_links = set()
    rows = []

    for role in roles:
        query = (
            f'site:linkedin.com "{role}" '
            '("NY NY" OR "New York City" OR NYC) '
            '("@gmail.com" OR "@yahoo.com" OR "@hotmail.com" OR "@outlook.com" OR "@aol.com" OR "@icloud.com")'
        )
        encoded_query = urllib.parse.quote_plus(query)

        print(f"\n🔍 Searching for: {query}")

        for page in range(PAGES):
            start = 1 + page * RESULTS_PER_PAGE
            url = (
                f"https://customsearch.googleapis.com/customsearch/v1?"
                f"key={API_KEY}&cx={CX}&q={encoded_query}&num={RESULTS_PER_PAGE}&start={start}"
            )

            print(f"Fetching: start={start} | URL: {url}")

            results = safe_request(url)

            # Debug full API result:
            print("\n=== RAW API RESPONSE ===")
            print(results)
            print("========================")

            if "error" in results:
                print("API Error:", results["error"])
                sys.exit(1)

            if "items" not in results:
                print(f"No results found for start={start}")
                break

            for item in results["items"]:
                link = item.get("link", "")
                if link in unique_links:
                    continue  # skip duplicates

                title = item.get("title", "")
                snippet = item.get("snippet", "")

                name = title.split("-")[0].strip()
                email = extract_email(snippet)
                location = "New York City"

                rows.append([name, location, email, link])
                unique_links.add(link)

                print(f"✅ Added: {name} | {email} | {link}")

            # Optional: short delay between requests to be polite
            time.sleep(1)

    # Write CSV once after all roles processed
    if rows:
        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Location", "Email", "Profile URL"])
            writer.writerows(rows)

        print(f"\n✅ Done! Saved {len(rows)} unique results to {OUTPUT_FILE}")
    else:
        print("⚠️ No results to save.")

if __name__ == "__main__":
    main()
