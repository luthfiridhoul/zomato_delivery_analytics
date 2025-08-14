
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from math import radians, cos, sin, asin, sqrt
from pathlib import Path

# ===================== PAGE / THEME =====================
st.set_page_config(
    page_title="Delivery Time Analytics",
    page_icon="🛵",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
:root {
  --bg: #0e1117;
  --card: #111827;
  --text: #e5e7eb;
  --muted: #94a3b8;
  --accent1: #22d3ee;
  --accent2: #a78bfa;
  --accent3: #34d399;
  --danger: #f43f5e;
}
html, body, [class*="css"]  { background-color: var(--bg); color: var(--text); }
.block-container { padding-top: 0.8rem; }
div.stMetric { background: linear-gradient(135deg, #111827, #0b1220); border-radius: 14px; padding: 10px; border: 1px solid #1f2937;}
section[data-testid="stSidebar"] { background: #0b1220; }
.stButton>button {
  border-radius: 10px;
  border: 1px solid #1f2937;
  background: linear-gradient(135deg, var(--accent2), var(--accent1));
  color: #0b0f16; font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ===================== LOAD DATA (same folder as this .py) =====================
DATA_FILENAME = "processed_zomato_dataset.xlsx"
data_path = Path.cwd() / DATA_FILENAME

if not data_path.exists():
    st.error(f"Data file '{DATA_FILENAME}' was not found in the same folder as this app.\n\n"
             f"Put the .xlsx next to this .py and rerun.")
    st.stop()

try:
    df = pd.read_excel(data_path)
except Exception as e:
    st.error(f"Failed to read '{DATA_FILENAME}': {e}")
    st.stop()

# ===================== COLUMN MAPPING =====================
EXPECTED_COLS = {
    "id": ["id", "order_id"],
    "delivery_person_id": ["delivery_person_id"],
    "delivery_person_age": ["delivery_person_age"],
    "delivery_person_ratings": ["delivery_person_ratings", "courier_rating", "rating"],
    "restaurant_latitude": ["restaurant_latitude", "rest_lat"],
    "restaurant_longitude": ["restaurant_longitude", "rest_lon", "rest_longitude"],
    "delivery_location_latitude": ["delivery_location_latitude", "dest_lat", "customer_latitude"],
    "delivery_location_longitude": ["delivery_location_longitude", "dest_lon", "customer_longitude"],
    "order_date": ["order_date", "date"],
    "time_orderd": ["time_orderd", "order_time"],
    "time_order_picked": ["time_order_picked", "pickup_time"],
    "weather_conditions": ["weather_conditions", "weather"],
    "road_traffic_density": ["road_traffic_density", "traffic_density", "traffic"],
    "vehicle_condition": ["vehicle_condition"],
    "type_of_order": ["type_of_order", "order_type"],
    "type_of_vehicle": ["type_of_vehicle", "vehicle_type"],
    "multiple_deliveries": ["multiple_deliveries", "multi_deliveries"],
    "festival": ["festival"],
    "city": ["city", "area"],
    "time_taken_min": ["time_taken (min)", "time_taken_min", "time_taken"]
}
def find_col(df, candidates):
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand in cols_lower:
            return cols_lower[cand]
    return None

colmap = {k: find_col(df, v) for k, v in EXPECTED_COLS.items()}
missing_critical = [k for k in ["order_date","time_taken_min"] if colmap.get(k) is None]
if missing_critical:
    st.error(f"Missing required columns: {missing_critical}")
    st.stop()

c = colmap

# ===================== CLEANING =====================
df[c["order_date"]] = pd.to_datetime(df[c["order_date"]], errors="coerce", dayfirst=True)
if c["time_orderd"]:
    try:
        ts = pd.to_datetime(df[c["order_date"]].dt.strftime("%Y-%m-%d") + " " + df[c["time_orderd"]].astype(str), errors="coerce")
        df["order_timestamp"] = ts
    except Exception:
        df["order_timestamp"] = df[c["order_date"]]
else:
    df["order_timestamp"] = df[c["order_date"]]

for numcol_key in ["time_taken_min","delivery_person_ratings","vehicle_condition","multiple_deliveries"]:
    colname = c.get(numcol_key)
    if colname:
        df[colname] = pd.to_numeric(df[colname], errors="coerce")

for k in ["weather_conditions","road_traffic_density","type_of_order","type_of_vehicle","festival","city"]:
    col = c.get(k)
    if col and col in df.columns:
        df[col] = df[col].astype(str).str.strip().fillna("Unknown")

# Optional distance if coordinates exist
def haversine_km(lat1, lon1, lat2, lon2):
    if np.isnan(lat1) or np.isnan(lon1) or np.isnan(lat2) or np.isnan(lon2):
        return np.nan
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c_ = 2 * np.arcsin(np.sqrt(a))
    return 6371 * c_

if all(c.get(k) for k in ["restaurant_latitude","restaurant_longitude","delivery_location_latitude","delivery_location_longitude"]):
    df["distance_km"] = [
        haversine_km(rlat, rlon, dlat, dlon)
        for rlat, rlon, dlat, dlon in zip(
            pd.to_numeric(df[c["restaurant_latitude"]], errors="coerce"),
            pd.to_numeric(df[c["restaurant_longitude"]], errors="coerce"),
            pd.to_numeric(df[c["delivery_location_latitude"]], errors="coerce"),
            pd.to_numeric(df[c["delivery_location_longitude"]], errors="coerce")
        )
    ]
else:
    df["distance_km"] = np.nan

# ===================== SIDEBAR FILTERS =====================
st.sidebar.markdown("### Filters")
sla = st.sidebar.slider("On‑Time threshold (minutes)", 15, 60, 30, 1)
f_city = st.sidebar.multiselect("City", sorted(df[c["city"]].dropna().unique().tolist()) if c.get("city") else [])
f_fest = st.sidebar.multiselect("Festival", sorted(df[c["festival"]].dropna().unique().tolist()) if c.get("festival") else [])
f_weat = st.sidebar.multiselect("Weather", sorted(df[c["weather_conditions"]].dropna().unique().tolist()) if c.get("weather_conditions") else [])
f_traf = st.sidebar.multiselect("Traffic", sorted(df[c["road_traffic_density"]].dropna().unique().tolist()) if c.get("road_traffic_density") else [])

mask = pd.Series(True, index=df.index)
if f_city:  mask &= df[c["city"]].isin(f_city)
if f_fest:  mask &= df[c["festival"]].isin(f_fest)
if f_weat:  mask &= df[c["weather_conditions"]].isin(f_weat)
if f_traf:  mask &= df[c["road_traffic_density"]].isin(f_traf)
dff = df[mask].copy()

# ===================== HEADER =====================
left, right = st.columns([0.75, 0.25])
with left:
    st.title("🛵 Delivery Time Analytics")
    st.caption("Single‑page insights on factors affecting delivery time.")
with right:
    st.metric("Rows (filtered)", f"{len(dff):,}")

# ===================== KPIs =====================
avg_time = dff[c["time_taken_min"]].mean()
total_orders = len(dff)
on_time = (dff[c["time_taken_min"]] <= sla).mean() if len(dff) else 0.0

k1,k2,k3,k4 = st.columns(4)
k1.metric("Average Delivery Time (min)", f"{avg_time:.1f}" if not np.isnan(avg_time) else "—")
k2.metric("Total Orders", f"{total_orders:,}")
k3.metric("On‑Time Delivery %", f"{on_time*100:.1f}%")
if "distance_km" in dff.columns and dff["distance_km"].notna().any():
    spd = (dff["distance_km"] / (dff[c["time_taken_min"]]/60)).replace([np.inf, -np.inf], np.nan).mean()
    k4.metric("Avg Speed (km/h)", f"{spd:.1f}" if not np.isnan(spd) else "—")
else:
    k4.metric("Avg Speed (km/h)", "—")

st.markdown("---")

# ===================== ROW 1: Trend & Heatmap =====================
r1c1, r1c2 = st.columns([0.55, 0.45])

with r1c1:
    st.subheader("Monthly Trend of Average Delivery Time")
    dff["_month"] = dff[c["order_date"]].dt.to_period("M").astype(str)
    trend = (
        dff.dropna(subset=[c["order_date"]])
          .groupby("_month", as_index=False)[c["time_taken_min"]]
          .mean()
          .rename(columns={c["time_taken_min"]: "Avg_Time"})
          .sort_values("_month")
    )
    if len(trend):
        fig = px.line(trend, x="_month", y="Avg_Time", markers=True, template="plotly_dark")
        fig.update_layout(xaxis_title="", yaxis_title="Minutes")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No date data available to plot trend.")

with r1c2:
    st.subheader("Impact of Weather and Traffic on Delivery Time")
    if c.get("weather_conditions") and c.get("road_traffic_density"):
        pivot = (
            dff.pivot_table(index=c["weather_conditions"], columns=c["road_traffic_density"],
                            values=c["time_taken_min"], aggfunc="mean")
        )
        if pivot.size > 0:
            figh = px.imshow(pivot, text_auto=True, aspect="auto", color_continuous_scale="RdYlGn_r", template="plotly_dark", labels={"color": "Time (min)"})
            figh.update_layout(xaxis_title="Traffic Density", yaxis_title="Weather")
            st.plotly_chart(figh, use_container_width=True)
        else:
            st.info("Not enough data for heatmap.")
    else:
        st.info("Weather/Traffic columns are missing for heatmap.")

# ===================== ROW 2: Operational Factors =====================
st.subheader("Operational Factors")

r2c1, r2c2 = st.columns(2)

with r2c1:
    st.markdown("**Average Delivery Time by Order Type**")
    if c.get("type_of_order"):
        order_agg = (
            dff.groupby(c["type_of_order"], as_index=False)[c["time_taken_min"]]
               .mean().rename(columns={c["time_taken_min"]: "Avg_Time"})
               .sort_values("Avg_Time", ascending=False)
        )
        fig1 = px.bar(order_agg, x=c["type_of_order"], y="Avg_Time", template="plotly_dark")
        fig1.update_layout(xaxis_title="Order Type", yaxis_title="Minutes")
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Column 'Type_of_order' is missing.")

with r2c2:
    st.markdown("**Average Delivery Time by Vehicle Type**")
    if c.get("type_of_vehicle"):
        veh_agg = (
            dff.groupby(c["type_of_vehicle"], as_index=False)[c["time_taken_min"]]
               .mean().rename(columns={c["time_taken_min"]: "Avg_Time"})
               .sort_values("Avg_Time", ascending=False)
        )
        fig2 = px.bar(veh_agg, x=c["type_of_vehicle"], y="Avg_Time", template="plotly_dark")
        fig2.update_layout(xaxis_title="Vehicle Type", yaxis_title="Minutes")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Column 'Type_of_vehicle' is missing.")

# ===================== ROW 3: Aggregated Scatter =====================
st.subheader("Relationship Between Courier Ratings and Delivery Time")
agg_level = st.selectbox("Aggregate by", options=[
    "Vehicle Condition", "Vehicle Type", "Order Type", "City", "None (raw points)"
], index=0)

x_rating_col = c.get("delivery_person_ratings")

if agg_level != "None (raw points)" and x_rating_col:
    group_col = None
    if agg_level == "Vehicle Condition" and c.get("vehicle_condition"):
        group_col = c["vehicle_condition"]
    elif agg_level == "Vehicle Type" and c.get("type_of_vehicle"):
        group_col = c["type_of_vehicle"]
    elif agg_level == "Order Type" and c.get("type_of_order"):
        group_col = c["type_of_order"]
    elif agg_level == "City" and c.get("city"):
        group_col = c["city"]

    if group_col is not None:
        agg = (
            dff.dropna(subset=[x_rating_col, c["time_taken_min"]])
               .groupby(group_col, as_index=False)
               .agg(avg_rating=(x_rating_col, "mean"),
                    avg_time=(c["time_taken_min"], "mean"))
        )
        if len(agg):
            figs = px.scatter(agg, x="avg_rating", y="avg_time", text=group_col, template="plotly_dark")
            figs.update_traces(textposition="top center")
            figs.update_layout(xaxis_title="Average Courier Rating", yaxis_title="Average Delivery Time (min)")
            st.plotly_chart(figs, use_container_width=True)
        else:
            st.info("Not enough data to aggregate.")
    else:
        st.info("Selected grouping column is not available in your dataset.")
elif x_rating_col:
    tmp = dff[[x_rating_col, c["time_taken_min"]]].dropna().copy()
    if len(tmp) > 2000:
        tmp = tmp.sample(2000, random_state=42)
    rng = np.random.default_rng(42)
    jitter = (rng.random(len(tmp)) - 0.5) * 0.1
    tmp["rating_jitter"] = pd.to_numeric(tmp[x_rating_col], errors="coerce") + jitter
    fig_raw = px.scatter(tmp, x="rating_jitter", y=c["time_taken_min"], opacity=0.5, template="plotly_dark")
    fig_raw.update_layout(xaxis_title="Courier Rating (jittered)", yaxis_title="Delivery Time (min)")
    st.plotly_chart(fig_raw, use_container_width=True)
else:
    st.info("Courier rating column not found; cannot render scatter.")

st.markdown("---")
st.caption("Built using Streamlit + Plotly.")
