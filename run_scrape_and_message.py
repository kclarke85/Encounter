#!/usr/bin/env python3
"""
CareRide LinkedIn Outreach — Nursing Home Directors, Metro Atlanta
Run this locally: python3 run_scrape_and_message.py
"""

import csv, time, sys, requests
from urllib.parse import quote_plus

APIFY_TOKEN    = "apify_api_Oclcm8xYhy5U5o0dRhWJWqaDmTotUX4hbtLj"
SCRAPER_ACTOR  = "curious_coder~linkedin-people-search-scraper"
MESSENGER_ACTOR = "apify~linkedin-message-sender"
OUTPUT_CSV     = "nursing_home_leads_atlanta.csv"
LOCATION       = "Atlanta, Georgia, United States"
MAX_PER_TERM   = 50

PITCH = (
    "Hi, this is Alex from Encounter Engineering. We just launched CareRide — "
    "it connects elderly patients to their families in real time during transport, "
    "with a full admin portal for documented insight. Three modes: patient, family, "
    "and administrator. Learn more at encounterengineering.org or call me back at "
    "470-404-5798."
)

SEARCH_TERMS = [
    ("nursing home director",      "nursing home director"),
    ("director of nursing",        "director of nursing"),
    ("nursing home administrator", "nursing home administrator"),
    ("assisted living director",   "assisted living director"),
]

OUTPUT_FIELDS = ["full_name","title","company","location","linkedin_url",
                 "summary","search_term","message_sent","message_status"]

def build_url(kw): 
    return (f"https://www.linkedin.com/search/results/people/"
            f"?keywords={quote_plus(kw)}&location={quote_plus(LOCATION)}&origin=FACETED_SEARCH")

def start_run(actor, payload):
    r = requests.post(f"https://api.apify.com/v2/acts/{actor}/runs",
                      params={"token": APIFY_TOKEN}, json=payload, timeout=30)
    r.raise_for_status()
    run_id = r.json()["data"]["id"]
    print(f"  → run {run_id}")
    return run_id

def wait(run_id, poll=12):
    while True:
        s = requests.get(f"https://api.apify.com/v2/actor-runs/{run_id}",
                         params={"token": APIFY_TOKEN}, timeout=20).json()["data"]["status"]
        print(f"  → {s}")
        if s == "SUCCEEDED": return True
        if s in ("FAILED","ABORTED","TIMED-OUT"): return False
        time.sleep(poll)

def fetch(run_id):
    return requests.get(f"https://api.apify.com/v2/actor-runs/{run_id}/dataset/items",
                        params={"token": APIFY_TOKEN,"format":"json","clean":"true"},
                        timeout=60).json()

def norm(item, term):
    f = item.get("firstName",""); l = item.get("lastName","")
    return {
        "full_name":  (item.get("name") or item.get("fullName") or f"{f} {l}").strip(),
        "title":      item.get("headline") or item.get("title") or "",
        "company":    item.get("companyName") or item.get("company") or "",
        "location":   item.get("location") or "",
        "linkedin_url": (item.get("linkedinUrl") or item.get("profileUrl") or "").strip().lower(),
        "summary":    item.get("summary") or "",
        "search_term": term,
        "message_sent": "", "message_status": "",
    }

# ── Phase 1: Scrape ──
print("=== PHASE 1: SCRAPING ===")
all_recs = {}
for label, kw in SEARCH_TERMS:
    print(f"\n[{label}]")
    try:
        rid = start_run(SCRAPER_ACTOR, {
            "searchUrl": build_url(kw), "maxResults": MAX_PER_TERM,
            "proxy": {"useApifyProxy": True, "apifyProxyGroups": ["RESIDENTIAL"]}
        })
        if not wait(rid): print("  ✗ failed"); continue
        items = fetch(rid)
        print(f"  ✓ {len(items)} results")
        for it in items:
            rec = norm(it, label)
            k = rec["linkedin_url"] or rec["full_name"].lower()
            if k and k not in all_recs:
                all_recs[k] = rec
    except Exception as e:
        print(f"  ✗ {e}")

records = list(all_recs.values())
print(f"\n── {len(records)} unique profiles ──")

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS, extrasaction="ignore")
    w.writeheader(); w.writerows(records)
print(f"✓ Saved {OUTPUT_CSV}")

if not records:
    print("No results — check Apify credits or broaden search."); sys.exit(1)

# ── Phase 2: Message ──
print("\n=== PHASE 2: OUTREACH ===")
li_at = input("Paste your LinkedIn li_at cookie (or press Enter to skip messaging): ").strip()
if not li_at:
    print("Skipped. Re-run with li_at to send messages.")
    sys.exit(0)

urls = [r["linkedin_url"] for r in records if r["linkedin_url"]]
print(f"Sending to {len(urls)} contacts...")
try:
    rid = start_run(MESSENGER_ACTOR, {
        "profileUrls": urls,
        "message": PITCH,
        "liAtCookie": li_at,
        "sendToConnections": True,
        "sendConnectionRequest": True,
        "connectionNote": PITCH[:300],
        "proxy": {"useApifyProxy": True, "apifyProxyGroups": ["RESIDENTIAL"]}
    })
    if wait(rid, poll=15):
        results = fetch(rid)
        smap = {(r.get("profileUrl") or r.get("linkedinUrl") or "").lower(): 
                r.get("status","sent") for r in results}
        for r in records:
            r["message_sent"] = PITCH
            r["message_status"] = smap.get(r["linkedin_url"], "not_attempted")
        sent = sum(1 for r in records if r["message_status"] not in ("","not_attempted","actor_failed","http_error"))
        print(f"\n✓ Done — {sent}/{len(records)} messages sent")
    else:
        print("Messenger run failed.")
except Exception as e:
    print(f"Messaging error: {e}")

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS, extrasaction="ignore")
    w.writeheader(); w.writerows(records)
print(f"✓ CSV updated: {OUTPUT_CSV}")
