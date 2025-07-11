from dateutil import parser as dateparser
from datetime import datetime, timezone

def split_past_future(events):
    now = datetime.now(timezone.utc)
    past, future = [], []
    for e in events:
        dt = dateparser.parse(e["termin"])
        (past if dt < now else future).append(e)
    return past, future

def diff_events(old_list, new_list):
    # build dicts keyed by URL (or other unique id)
    old_map = {e["link"]: e for e in old_list}
    new_map = {e["link"]: e for e in new_list}

    added = [e for u,e in new_map.items() if u not in old_map]
    dropped = [e for u,e in old_map.items() if u not in new_map]
    changed = []
    for u in set(old_map) & set(new_map):
        if old_map[u] != new_map[u]:
            changed.append({"before": old_map[u], "after": new_map[u]})
    return {"added": added, "dropped": dropped, "changed": changed}
