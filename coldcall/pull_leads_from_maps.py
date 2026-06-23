import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import click, requests, time
from datetime import datetime, timezone
from rich.console import Console
from rich.table import Table
from config import leads_col

console = Console()

APIFY_BASE = "https://api.apify.com/v2"
ACTOR_ID   = "nwua9Gu5YrADL7ZDj"  # Google Maps Scraper actor

def run_maps_scrape(query, location, max_results, api_token):
    """Start an Apify actor run and wait for results."""

    run_input = {
        "searchStringsArray": [query],
        "locationQuery": location,
        "maxCrawledPlacesPerSearch": max_results,
        "language": "en",
        "countryCode": "us",
        "includeWebResults": False,
    }

    console.print(f"  Starting Apify Maps scrape...")
    resp = requests.post(
        f"{APIFY_BASE}/acts/{ACTOR_ID}/runs",
        params={"token": api_token},
        json={"runInput": run_input},
    )
    if resp.status_code != 201:
        console.print(f"[red]APIFY ERROR {resp.status_code}:[/red] {resp.text}")
        resp.raise_for_status()

    run_id = resp.json()["data"]["id"]
    console.print(f"  Run started: [cyan]{run_id}[/cyan]")

    # Poll until finished
    while True:
        status_resp = requests.get(
            f"{APIFY_BASE}/actor-runs/{run_id}",
            params={"token": api_token},
        )
        status = status_resp.json()["data"]["status"]
        if status == "SUCCEEDED":
            break
        elif status in ("FAILED", "ABORTED", "TIMED-OUT"):
            console.print(f"[red]Run {status}[/red]")
            return []
        console.print(f"  Status: [yellow]{status}[/yellow] — waiting 5s...")
        time.sleep(5)

    # Fetch results
    dataset_id = status_resp.json()["data"]["defaultDatasetId"]
    items_resp = requests.get(
        f"{APIFY_BASE}/datasets/{dataset_id}/items",
        params={"token": api_token, "format": "json", "clean": True},
    )
    return items_resp.json()

def normalize(place):
    """Map Google Maps place to our lead schema."""
    name  = place.get("title", "")
    phone = place.get("phone", "") or place.get("phoneUnformatted", "")

    # Normalize phone to E.164 (+1XXXXXXXXXX)
    if phone:
        digits = "".join(c for c in phone if c.isdigit())
        if len(digits) == 10:
            phone = f"+1{digits}"
        elif len(digits) == 11 and digits.startswith("1"):
            phone = f"+{digits}"
        else:
            phone = None

    return {
        "apollo_id":    place.get("placeId"),     # reuse apollo_id field for dedup
        "name":         "Administrator",           # title — unknown from Maps
        "first_name":   "Administrator",
        "last_name":    "",
        "title":        "Administrator",
        "company":      name,
        "industry":     "nursing home",
        "phone":        phone,
        "email":        place.get("website", ""),
        "city":         place.get("city", ""),
        "state":        place.get("state", ""),
        "address":      place.get("address", ""),
        "rating":       place.get("totalScore"),
        "reviews":      place.get("reviewsCount"),
        "website":      place.get("website", ""),
        "maps_url":     place.get("url", ""),
        "status":       "new" if phone else "no_phone",
        "source":       "google_maps",
        "created_at":   datetime.now(timezone.utc),
        "called_at":    None,
        "call_id":      None,
        "call_outcome": None,
    }

@click.command()
@click.option("--query",    default="nursing home",    help="Search query")
@click.option("--location", default="Atlanta, Georgia", help="Location to search")
@click.option("--limit",    default=20,                help="Max results to fetch")
@click.option("--token",    default=None,              help="Apify API token (or set APIFY_TOKEN in .env)")
@click.option("--dry-run",  is_flag=True,              help="Preview without saving")
def main(query, location, limit, token, dry_run):
    from dotenv import load_dotenv
    load_dotenv()
    api_token = token or os.getenv("APIFY_TOKEN")
    if not api_token:
        console.print("[red]No Apify token. Pass --token or set APIFY_TOKEN in .env[/red]")
        return

    console.print(f"\n[bold]Google Maps lead pull[/bold]")
    console.print(f"  Query:    [cyan]{query}[/cyan]")
    console.print(f"  Location: [cyan]{location}[/cyan]")
    console.print(f"  Limit:    [cyan]{limit}[/cyan]\n")

    places = run_maps_scrape(query, location, limit, api_token)
    console.print(f"\n  Raw results: [cyan]{len(places)}[/cyan]")

    leads       = [normalize(p) for p in places]
    with_phone  = [l for l in leads if l["phone"]]
    no_phone    = [l for l in leads if not l["phone"]]

    console.print(f"  With phone: [green]{len(with_phone)}[/green]")
    console.print(f"  No phone:   [yellow]{len(no_phone)}[/yellow]\n")

    table = Table(show_header=True, header_style="bold")
    for col in ["Facility", "Phone", "City", "Rating"]:
        table.add_column(col)
    for l in with_phone[:15]:
        table.add_row(
            (l["company"] or "")[:40],
            l["phone"] or "",
            l["city"] or "",
            str(l["rating"] or ""),
        )
    console.print(table)
    if len(with_phone) > 15:
        console.print(f"[dim]...and {len(with_phone)-15} more[/dim]")

    if dry_run:
        console.print("\n[yellow]Dry run - nothing saved.[/yellow]")
        return

    col   = leads_col()
    saved = 0
    dupes = 0
    for l in with_phone:
        if col.find_one({"apollo_id": l["apollo_id"]}):
            dupes += 1
        else:
            col.insert_one(l)
            saved += 1

    console.print(f"\n[green]Saved {saved} new leads.[/green] Skipped {dupes} duplicates.")
    console.print(f"Run campaign: [bold]python run_campaign.py --batch {saved} --dry-run[/bold]")

if __name__ == "__main__":
    main()
