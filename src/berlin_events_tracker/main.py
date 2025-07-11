from .fetcher import fetch_all_events
from .parser import parse_articles_from_html
from .storage import load, save
from .comparator import split_past_future, diff_events
from .notifier import notify_new_events

def run():
    # 1. Load yesterday’s “today_events”
    yesterday = load("yesterday_events")

    # 2. Fetch + parse today’s events
    today = fetch_all_events()

    # 3. Split yesterday into past vs still-future
    past_yest, future_yest = split_past_future(yesterday)

    # 4. Append all past_yest to past_events file
    past = load("past_events")
    past.extend(past_yest)
    save("past_events", past)

    # 5. Compare future_yest against today
    delta = diff_events(future_yest, today)
    save("diff_events", delta)

    # 6. Overwrite yesterday_events with today
    save("yesterday_events", today)

    # 7. Always save today_events if you want a snapshot
    save("today_events", today)

    print("Run complete. Past:", len(past_yest),
          "Added:", len(delta["added"]),
          "Dropped:", len(delta["dropped"]),
          "Changed:", len(delta["changed"]))
    
    # 8. Notify about new events
    added = delta.get("added", [])
    notify_new_events(added)