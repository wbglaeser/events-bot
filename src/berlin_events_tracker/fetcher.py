import requests
import time, random
from .parser import parse_articles_from_html

BASE_URL = "https://www.berlin.de/tickets/suche/"
COMMON_PARAMS = {
    "order_by": "start",
    "categories[]": [
        "Bildung & Vorträge", "Comedy", "Filmfestivals",
    ],
}

def fetch_events(offset=0, limit=50):
    """Return a list of HTML‐blobs (or JSON objects) of events for one page."""
    params = COMMON_PARAMS.copy()
    params.update({"offset": offset, "limit": limit})
    resp = requests.get(BASE_URL, params=params)
    resp.raise_for_status()
    return resp.text

def fetch_all_events(batch_size=50):
    offset = 0
    all_events = []
    last_batch = []
    while True:
        print(f"Fetching events from offset {offset} with batch size {batch_size}")
        html = fetch_events(offset=offset, limit=batch_size)
        items = parse_articles_from_html(html)
        if not items:
            break
        if [item['title'] for item in items] == [item['title'] for item in last_batch]:
            print("No new items found, stopping fetch.")
            break
        last_batch = items
        all_events.extend(items)
        offset += batch_size
        time.sleep(random.uniform(1, 2))
    return all_events