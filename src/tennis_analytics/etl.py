from .api import fetch_feed
from .db import init_db, upsert, save_rankings, Category, Competition, Complex, Venue
from .parsers import parse_competitions, parse_complexes, parse_rankings

def collect_all():
    init_db()
    categories, competitions = parse_competitions(fetch_feed("competitions"))
    upsert(Category, categories, "category_id")
    upsert(Competition, competitions, "competition_id")
    complexes, venues = parse_complexes(fetch_feed("complexes"))
    upsert(Complex, complexes, "complex_id")
    upsert(Venue, venues, "venue_id")
    players, rankings = parse_rankings(fetch_feed("double_competitors_rankings"))
    save_rankings(players, rankings)
    return {"categories": len(categories), "competitions": len(competitions),
            "complexes": len(complexes), "venues": len(venues),
            "competitors": len(players), "ranking_rows": len(rankings)}
