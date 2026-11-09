import json

def raw(obj):
    return json.dumps(obj, ensure_ascii=False)

def parse_competitions(payload):
    categories, competitions = {}, {}
    for item in payload.get("competitions", []) or []:
        cat = item.get("category") or {}
        if cat.get("id"):
            categories[str(cat["id"])] = {
                "category_id": str(cat["id"]),
                "category_name": cat.get("name") or "Unknown"
            }
        if item.get("id"):
            cid = str(item["id"])
            competitions[cid] = {
                "competition_id": cid,
                "competition_name": item.get("name") or "Unknown",
                "parent_id": item.get("parent_id"),
                "type": item.get("type") or "unknown",
                "gender": item.get("gender") or "unknown",
                "level": item.get("level"),
                "category_id": str(cat["id"]) if cat.get("id") else None,
                "raw_json": raw(item)
            }
    return list(categories.values()), list(competitions.values())

def parse_complexes(payload):
    complexes, venues = [], []
    for item in payload.get("complexes", []) or []:
        if not item.get("id"):
            continue
        xid = str(item["id"])
        complexes.append({"complex_id": xid, "complex_name": item.get("name") or "Unknown",
                          "raw_json": raw(item)})
        for v in item.get("venues", []) or []:
            if v.get("id"):
                venues.append({
                    "venue_id": str(v["id"]), "venue_name": v.get("name") or "Unknown",
                    "city_name": v.get("city_name") or "Unknown",
                    "country_name": v.get("country_name") or "Unknown",
                    "country_code": v.get("country_code"), "timezone": v.get("timezone") or "Unknown",
                    "complex_id": xid, "raw_json": raw(v)
                })
    return complexes, venues

def parse_rankings(payload):
    competitors, rankings = {}, []
    groups = payload.get("rankings") or [payload]
    for group in groups:
        entries = group.get("competitor_rankings") or group.get("rankings") or []
        for item in entries:
            p = item.get("competitor") or {}
            if not p.get("id"):
                continue
            pid = str(p["id"])
            competitors[pid] = {
                "competitor_id": pid, "name": p.get("name") or "Unknown",
                "country": p.get("country") or "Unknown", "country_code": p.get("country_code"),
                "abbreviation": p.get("abbreviation"), "raw_json": raw(p)
            }
            if item.get("rank") is not None:
                rankings.append({
                    "rank": int(item["rank"]), "movement": int(item.get("movement") or 0),
                    "points": int(item.get("points") or 0),
                    "competitions_played": int(item.get("competitions_played") or 0),
                    "competitor_id": pid, "ranking_type": group.get("type") or "doubles",
                    "raw_json": raw(item)
                })
    return list(competitors.values()), rankings
