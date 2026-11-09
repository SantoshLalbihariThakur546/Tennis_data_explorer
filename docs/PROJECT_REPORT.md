# Project Report — Game Analytics: Unlocking Tennis Data with Sportradar API

## Introduction
This application retrieves tennis competition, complex/venue, and doubles competitor ranking feeds. Python performs extraction and JSON transformation, SQL stores normalized records, and Streamlit presents interactive analysis.

## Objectives
- Integrate Sportradar Tennis API feeds.
- Normalize nested JSON into relational tables.
- Preserve category, parent competition, complex, venue, and competitor relationships.
- Execute SQL queries for competition, venue, and ranking analysis.
- Build a dashboard with KPIs, filters, charts, and leaderboards.
- Test, document, and publish the project using GitHub.

## Technology
Python, Requests, SQLAlchemy, MySQL/SQLite, Pandas, Plotly, Streamlit, Pytest, Git and GitHub.

## Data model
Six tables: categories, competitions, complexes, venues, competitors, competitor_rankings. Categories link to competitions; complexes link to venues; competitors link to ranking records. Competition parent IDs represent hierarchy. Indexes support common category, type, country and ranking filters.

## Workflow
1. Configure API credentials securely.
2. Request JSON feeds using the x-api-key header.
3. Validate HTTP responses and parse JSON.
4. Flatten nested categories, venues and competitors.
5. Upsert entity data and refresh the current ranking snapshot.
6. Query the database and render Streamlit views.

## Dashboard
Overview KPIs; doubles ranking filters and CSV export; country-wise analysis; competition explorer; venue explorer.

## Testing and security
Parser tests use representative fixtures and do not require a live key. Run `pytest -q`. Credentials belong in `.env` or Streamlit secrets, never in Git. API access, rate limits and coverage depend on the Sportradar account.

## Limitations
The stored rankings represent the latest fetched snapshot rather than a historical time series. Feed coverage varies by subscription. Verify actual response shapes against the current account documentation. For persistent cloud deployment, use a managed database rather than ephemeral local SQLite.

## Conclusion
The project demonstrates API extraction, JSON transformation, relational database design, SQL analytics, interactive visualization, automated testing and cloud deployment.
