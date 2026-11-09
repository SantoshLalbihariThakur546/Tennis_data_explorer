# Tennis Data Explorer — Game Analytics

End-to-end capstone: Sportradar Tennis API → Python ETL → MySQL/SQLite → SQL analytics → Streamlit dashboard.

## Setup
1. Install Python 3.10+ and (optionally) MySQL 8+.
2. Create and activate a virtual environment:
   - Windows: `py -m venv .venv` then `.venv\Scripts\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
3. Install: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env`, then add your own Sportradar API key.
5. Initialize: `python scripts/init_db.py`
6. Collect: `python scripts/collect_all.py`
7. Run: `streamlit run app.py`
8. Test: `pytest -q`

Default database is SQLite for easy local testing. For MySQL, set:
`DATABASE_URL=mysql+pymysql://user:password@localhost:3306/tennis_analytics`

## Configuration
`SPORTRADAR_API_KEY`, `SPORTRADAR_ACCESS_LEVEL=trial|production`, `SPORTRADAR_LANGUAGE=en`, `DATABASE_URL`.
Never commit `.env`. A real API key and relevant feed entitlements are required. API quota and coverage depend on your Sportradar account.

## Feeds
- `competitions.json`
- `complexes.json`
- `double_competitors_rankings.json`

Requests use the `x-api-key` header and the Tennis API v3 URL pattern:
`https://api.sportradar.com/tennis/{access_level}/v3/{language}/{feed}.json`

## GitHub
`git init && git add . && git commit -m "Build Tennis Data Explorer"`
Create an empty GitHub repository, then add its URL as `origin` and push `main`.

## Streamlit Community Cloud
Push to GitHub, create an app from the repository with `app.py` as entry point, and add secrets in App settings:
```toml
SPORTRADAR_API_KEY = "your-key"
SPORTRADAR_ACCESS_LEVEL = "trial"
SPORTRADAR_LANGUAGE = "en"
DATABASE_URL = "sqlite:///tennis_analytics.db"
```
For durable public deployment use a managed MySQL/PostgreSQL database; hosted local SQLite storage is not a reliable persistent production database.

## Database tables
`categories`, `competitions`, `complexes`, `venues`, `competitors`, `competitor_rankings`.
Ranking data is stored as a latest snapshot. Feed fields can vary with API version/access; inspect your actual JSON response and adjust parsers if Sportradar changes its schema.
