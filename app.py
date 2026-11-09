import streamlit as st
import plotly.express as px
from src.tennis_analytics.db import init_db
from src.tennis_analytics.etl import collect_all
from src.tennis_analytics.api import APIError
from src.tennis_analytics.queries import kpis, ranking_rows, country_stats, competitions, venues, countries

st.set_page_config(page_title="Tennis Data Explorer", page_icon="🎾", layout="wide")
init_db()
st.title("🎾 Tennis Data Explorer")
st.caption("Game Analytics | Unlocking Tennis Data with Sportradar API")

with st.sidebar:
    page = st.radio("Navigation", ["Overview", "Competitor Rankings", "Country Analysis", "Competitions", "Venues"])
    st.divider()
    if st.button("↻ Sync Sportradar data", use_container_width=True):
        with st.spinner("Downloading and storing feeds..."):
            try:
                result = collect_all()
                st.success("Synchronization complete")
                st.json(result)
                st.cache_data.clear()
            except APIError as e:
                st.error(str(e))
            except Exception as e:
                st.exception(e)

@st.cache_data(ttl=60)
def load_kpis():
    return kpis()

if page == "Overview":
    st.subheader("Project overview")
    try:
        k = load_kpis()
        cols = st.columns(5)
        for col, label, key in zip(cols, ["Competitors","Countries","Highest points","Competitions","Venues"],
                                   ["competitors","countries","highest_points","competitions","venues"]):
            col.metric(label, f"{int(k[key]):,}")
        st.divider()
        a, b = st.columns(2)
        with a:
            c = country_stats()
            st.markdown("#### Competitors by country")
            if not c.empty: st.plotly_chart(px.bar(c.head(15), x="country", y="competitors"), use_container_width=True)
            else: st.info("No data yet. Configure your key and sync.")
        with b:
            d = competitions()
            st.markdown("#### Competition types")
            if not d.empty:
                chart = d.groupby(["category_name","type"], dropna=False).size().reset_index(name="count")
                st.plotly_chart(px.bar(chart, x="category_name", y="count", color="type", barmode="group"), use_container_width=True)
            else: st.info("No competition records loaded.")
    except Exception as e:
        st.warning(f"Database initialized; data not available yet. {e}")

elif page == "Competitor Rankings":
    st.subheader("Doubles competitor leaderboard")
    cs = ["All"] + countries()
    a,b,c,d = st.columns(4)
    country = a.selectbox("Country", cs)
    lo = b.number_input("Minimum rank", 1, 500, 1)
    hi = c.number_input("Maximum rank", 1, 500, 500)
    pts = d.number_input("Minimum points", 0, value=0)
    if lo > hi: st.error("Minimum rank cannot exceed maximum rank.")
    else:
        data = ranking_rows(None if country == "All" else country, lo, hi, pts)
        st.dataframe(data, use_container_width=True, hide_index=True)
        if not data.empty: st.download_button("Export CSV", data.to_csv(index=False), "rankings.csv", "text/csv")

elif page == "Country Analysis":
    st.subheader("Country-wise performance")
    data = country_stats()
    if data.empty: st.info("No data loaded.")
    else:
        st.dataframe(data, use_container_width=True, hide_index=True)
        st.plotly_chart(px.bar(data.head(20), x="country", y="average_points"), use_container_width=True)

elif page == "Competitions":
    st.subheader("Competition explorer")
    data = competitions()
    if data.empty: st.info("No competitions loaded.")
    else:
        types = ["All"] + sorted(data["type"].dropna().unique().tolist())
        selected = st.selectbox("Competition type", types)
        if selected != "All": data = data[data["type"] == selected]
        st.dataframe(data, use_container_width=True, hide_index=True)

elif page == "Venues":
    st.subheader("Complexes and venues")
    data = venues()
    if data.empty: st.info("No venues loaded.")
    else:
        cs = ["All"] + sorted(data["country_name"].dropna().unique().tolist())
        selected = st.selectbox("Country", cs)
        if selected != "All": data = data[data["country_name"] == selected]
        st.dataframe(data, use_container_width=True, hide_index=True)

st.divider()
st.caption("Feed availability depends on Sportradar subscription and data coverage.")
