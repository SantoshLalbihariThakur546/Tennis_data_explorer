import pandas as pd
from sqlalchemy import text
from .db import engine

def df(sql, params=None):
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn, params=params or {})

def kpis():
    return df("SELECT (SELECT COUNT(*) FROM competitors) competitors, "
              "(SELECT COUNT(DISTINCT country) FROM competitors) countries, "
              "(SELECT COALESCE(MAX(points),0) FROM competitor_rankings) highest_points, "
              "(SELECT COUNT(*) FROM competitions) competitions, "
              "(SELECT COUNT(*) FROM venues) venues").iloc[0]

def ranking_rows(country=None, min_rank=1, max_rank=500, min_points=0):
    return df("""SELECT r.rank, p.name, p.country, r.movement, r.points,
             r.competitions_played FROM competitor_rankings r
             JOIN competitors p ON p.competitor_id=r.competitor_id
             WHERE (:country IS NULL OR p.country=:country)
             AND r.rank BETWEEN :lo AND :hi AND r.points >= :pts ORDER BY r.rank""",
             {"country": country, "lo": min_rank, "hi": max_rank, "pts": min_points})

def country_stats():
    return df("""SELECT p.country, COUNT(*) competitors, ROUND(AVG(r.points),1) average_points,
             SUM(r.points) total_points FROM competitors p JOIN competitor_rankings r
             ON r.competitor_id=p.competitor_id GROUP BY p.country ORDER BY competitors DESC""")

def competitions():
    return df("""SELECT c.competition_name, c.type, c.gender, c.level, c.parent_id,
             a.category_name FROM competitions c LEFT JOIN categories a
             ON a.category_id=c.category_id ORDER BY a.category_name,c.competition_name""")

def venues():
    return df("""SELECT v.venue_name,v.city_name,v.country_name,v.country_code,v.timezone,
             x.complex_name FROM venues v JOIN complexes x ON x.complex_id=v.complex_id
             ORDER BY v.country_name,v.venue_name""")

def countries():
    return df("SELECT DISTINCT country FROM competitors ORDER BY country")["country"].tolist()
