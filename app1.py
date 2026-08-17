import streamlit as st
import pandas as pd

# =========================
# CUSTOM DASHBOARD STYLE
# =========================

st.markdown("""
<style>

.home-card {
    background: linear-gradient(135deg, #151b25, #1d2633);
    border: 1px solid #303a4a;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 18px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.22);
}

.home-card h3 {
    margin-top: 0;
    font-size: 21px;
}

.home-card p {
    color: #c8ced8;
    font-size: 15px;
    line-height: 1.6;
}

.project-badge {
    display: inline-block;
    background: #1d4f73;
    color: #e8f4ff;
    padding: 6px 13px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 12px;
}

.feature-card {
    background: #151b25;
    border: 1px solid #303a4a;
    border-radius: 14px;
    padding: 20px;
    min-height: 145px;
}

.feature-card h4 {
    margin-top: 0;
    font-size: 18px;
}

.feature-card p {
    color: #b9c1cc;
    font-size: 14px;
    line-height: 1.5;
}

.footer-box {
    text-align: center;
    color: #8993a3;
    font-size: 13px;
    padding: 25px 0 10px 0;
}

</style>
""", unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    page_title="Supply Chain Demand Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load historical and anomaly dataset
historical_df = pd.read_excel(
    "data/final_anomaly_dataset (1).xlsx"
)

# Convert Date column to datetime
historical_df["Date"] = pd.to_datetime(
    historical_df["Date"]
)

# Load anomaly detection dataset
anomaly_df = pd.read_excel(
    "data/final_anomaly_dataset (1).xlsx"
)

# Convert Date column to datetime
anomaly_df["Date"] = pd.to_datetime(anomaly_df["Date"])

# Sort by Date
anomaly_df = anomaly_df.sort_values("Date")

# Load forecast dataset
forecast_df = pd.read_excel("data/future_forecast.xlsx")
forecast_df["Date"] = pd.to_datetime(forecast_df["Date"])

forecast_df["Forecast"] = forecast_df["Forecast"].round(2)
# Main dataframe
df = historical_df.copy()

# Sidebar
st.sidebar.markdown("---")
st.sidebar.title(" Navigation")
st.sidebar.caption("Supply Chain Analytics")

st.sidebar.markdown("---")
st.sidebar.subheader(" Filters")

# Region Filter
region_options = ["All"] + sorted(df["Region"].dropna().unique().tolist())
selected_region = st.sidebar.selectbox(
    "Select Region",
    region_options
)

# Category Filter
category_options = ["All"] + sorted(df["Category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox(
    "Select Category",
    category_options
)

# Store Filter
store_options = ["All"] + sorted(df["Store ID"].dropna().unique().tolist())
selected_store = st.sidebar.selectbox(
    "Select Store",
    store_options
)
filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]

if selected_store != "All":
    filtered_df = filtered_df[
        filtered_df["Store ID"] == selected_store
    ]
filtered_anomaly_df = anomaly_df.copy()

if selected_region != "All":
    filtered_anomaly_df = filtered_anomaly_df[
        filtered_anomaly_df["Region"] == selected_region
    ]

if selected_category != "All":
    filtered_anomaly_df = filtered_anomaly_df[
        filtered_anomaly_df["Category"] == selected_category
    ]

if selected_store != "All":
    filtered_anomaly_df = filtered_anomaly_df[
        filtered_anomaly_df["Store ID"] == selected_store
    ]
# =========================
# FILTER VALIDATION
# =========================

if filtered_df.empty:
    st.warning(
        "No historical records found for the selected filters."
    )

if filtered_anomaly_df.empty:
    st.info(
        "No anomaly records found for the selected filters."
    )

page = st.sidebar.radio(
    "Select Section",
    [
        "Home",
        "Historical Demand",
        "Anomaly Detection",
        "Forecast"
    ]
)


# =========================
# PAGE CONTENT
# =========================

if page == "Home":

    st.markdown(
        '<span class="project-badge">SUPPLY CHAIN ANALYTICS</span>',
        unsafe_allow_html=True
    )

    st.header("Welcome to the Demand Analytics Dashboard")

    st.write(
        "Explore historical demand patterns, anomaly detection results, "
        "and future demand forecasts through an interactive analytics interface."
    )

    # Project Overview
    st.markdown("""
    <div class="home-card">
        <h3>Project Overview</h3>
        <p>
        This dashboard integrates historical demand data, anomaly detection
        results, and 90-day demand forecasting into a single interactive
        Streamlit application.
        </p>
        <p>
        Use the navigation panel and filters to explore the available
        supply chain data and analytical results.
        </p>
    </div>
    """, unsafe_allow_html=True)

elif page == "Historical Demand":

    st.header("Historical Demand")

    st.markdown("""
    <div class="home-card">

    <h3>Historical Demand Overview</h3>

    <p>
    Explore daily demand based on Units Sold. Use the sidebar filters
    to analyze demand for a specific region, category, or store.
    </p>

    </div>
    """, unsafe_allow_html=True)

elif page == "Anomaly Detection":

    st.header("Anomaly Detection")

    st.markdown("""
    <div class="home-card">

    <h3>Anomaly Detection Overview</h3>

    <p>
    Review unusual demand records identified using three anomaly
    detection techniques: IQR, Isolation Forest, and Z-Score.
    </p>

    <p>
    The displayed results are updated according to the selected
    Region, Category, and Store filters.
    </p>

    </div>
    """, unsafe_allow_html=True)

elif page == "Forecast":

    st.header("Demand Forecast")

    st.markdown("""
    <div class="home-card">

    <h3>90-Day Demand Forecast Overview</h3>

    <p>
    View the demand predictions generated by the advanced forecasting
    model for the upcoming 90-day period.
    </p>

    <p>
    The forecast data and summary statistics provide an overview
    of expected future demand.
    </p>

    </div>
    """, unsafe_allow_html=True)