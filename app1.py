import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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

# =========================
# LOAD DATASETS
# =========================

@st.cache_data
def load_data():

    # Main historical + anomaly dataset
    historical_df = pd.read_excel(
        "data/final_anomaly_dataset (1).xlsx"
    )

    historical_df["Date"] = pd.to_datetime(
        historical_df["Date"]
    )

    # Forecast dataset
    forecast_df = pd.read_excel(
        "data/future_forecast.xlsx"
    )

    forecast_df["Date"] = pd.to_datetime(
        forecast_df["Date"]
    )

    forecast_df["Forecast"] = pd.to_numeric(
        forecast_df["Forecast"],
        errors="coerce"
    )

    forecast_df = forecast_df.dropna(
        subset=["Date", "Forecast"]
    ).sort_values("Date")

    forecast_df["Forecast"] = forecast_df["Forecast"].round(2)

    # Advanced ARIMA forecast
    advanced_forecast_df = pd.read_excel(
        "data/advanced_forecast.xlsx"
    )

    advanced_forecast_df["Date"] = pd.to_datetime(
        advanced_forecast_df["Date"]
    )

    advanced_forecast_df["Actual"] = pd.to_numeric(
        advanced_forecast_df["Actual"],
        errors="coerce"
    )

    advanced_forecast_df["ARIMA_Prediction"] = pd.to_numeric(
        advanced_forecast_df["ARIMA_Prediction"],
        errors="coerce"
    )

    advanced_forecast_df = advanced_forecast_df.dropna(
        subset=[
            "Date",
            "Actual",
            "ARIMA_Prediction"
        ]
    ).sort_values("Date")

    return (
        historical_df,
        forecast_df,
        advanced_forecast_df
    )


historical_df, forecast_df, advanced_forecast_df = load_data()

# Use the same loaded dataset for analysis
anomaly_df = historical_df.copy()
anomaly_df = anomaly_df.sort_values("Date")

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
# TOP KPI CARDS
# =========================

col1, col2, col3 = st.columns(3, gap="medium")

# Anomaly count based on selected filters
anomaly_count = (
    (filtered_anomaly_df["IQR_Anomaly"] == 1) |
    (filtered_anomaly_df["IsolationForest"] == 1) |
    (filtered_anomaly_df["ZScore_Anomaly"] == 1)
).sum()

with col1:
    st.metric(
        "Historical Records",
        f"{len(filtered_df):,}"
    )

with col2:
    st.metric(
        "Anomaly Records",
        f"{anomaly_count:,}"
    )

with col3:
    st.metric(
        "Forecast Days",
        f"{len(forecast_df):,}"
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

    # Forecast Overview
    st.subheader("Forecast Overview")

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.metric(
            "Forecast Records",
            f"{len(forecast_df):,}"
        )

    with col2:
        st.metric(
            "Average Forecast",
            f"{forecast_df['Forecast'].mean():,.2f}"
        )

    with col3:
        st.metric(
            "Maximum Forecast",
            f"{forecast_df['Forecast'].max():,.2f}"
        )

    # Dashboard Features
    st.subheader("Dashboard Features")

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>Historical Demand</h4>
            <p>
            Explore historical demand records, units sold,
            summary statistics, and filtered demand data.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>Anomaly Detection</h4>
            <p>
            Review detected anomalies using IQR,
            Isolation Forest, and Z-Score analysis.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>Demand Forecast</h4>
            <p>
            View the available 90-day demand forecast
            and forecast summary statistics.
            </p>
        </div>
        """, unsafe_allow_html=True)
    # =========================
    # DASHBOARD STATUS
    # =========================

    st.subheader("Dashboard Overview")

    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>Data Integration</h4>
            <p>
            Historical demand, anomaly detection, and forecast
            datasets are integrated into one dashboard.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>Interactive Filters</h4>
            <p>
            Filter the dashboard using Region, Category,
            and Store to explore specific records.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>Analytical Summary</h4>
            <p>
            View demand statistics, anomaly counts,
            and forecast summary information.
            </p>
        </div>
        """, unsafe_allow_html=True)

# How to Use
    st.subheader("How to Use")

    st.info(
        "Select a Region, Category, and Store from the sidebar. "
        "Then choose Historical Demand, Anomaly Detection, or Forecast "
        "to explore the corresponding analysis."
    )

    st.markdown("""
    <div class="footer-box">
        Supply Chain Analytics • Demand Forecasting Dashboard
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

    # Summary statistics
    total_sales = filtered_df["Units Sold"].sum()
    average_sales = filtered_df["Units Sold"].mean()
    maximum_sales = filtered_df["Units Sold"].max()
    minimum_sales = filtered_df["Units Sold"].min()
    total_records = len(filtered_df)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Units Sold", f"{total_sales:,.0f}")

    with col2:
        st.metric("Average Units Sold", f"{average_sales:,.2f}")

    with col3:
        st.metric("Maximum Units Sold", f"{maximum_sales:,.0f}")

    with col4:
        st.metric("Minimum Units Sold", f"{minimum_sales:,.0f}")

    with col5:
        st.metric("Total Records", f"{total_records:,}")

    st.subheader("Historical Demand Data")
    st.caption(
    "Showing records based on the currently selected Region, Category, and Store filters."
     )

    st.dataframe(
        filtered_df[
            [
                "Date",
                "Store ID",
                "Product ID",
                "Category",
                "Region",
                "Units Sold"
            ]
        ],
        use_container_width=True
    )
    # =========================
    # HISTORICAL DEMAND CHART
    # =========================

    st.subheader("Historical Demand Trend")

    st.caption(
    "Daily total units sold based on the selected Region, Category, and Store filters."
    )

    historical_chart_df = (
    filtered_df
    .groupby("Date", as_index=False)["Units Sold"]
    .sum()
    .sort_values("Date")
    )

    # Interactive historical demand chart
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=historical_chart_df["Date"],
            y=historical_chart_df["Units Sold"],
            mode="lines",
            name="Historical Demand",
            line=dict(width=2),
            hovertemplate=
                "Date: %{x|%d %b %Y}<br>"
                "Units Sold: %{y:,.0f}<extra></extra>"
        )
    )

    fig.update_layout(
        height=500,
        xaxis_title="Date",
        yaxis_title="Units Sold",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=30, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

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

    st.subheader("Anomaly Summary")

    iqr_count = filtered_anomaly_df["IQR_Anomaly"].sum()
    isolation_count = filtered_anomaly_df["IsolationForest"].sum()
    zscore_count = filtered_anomaly_df["ZScore_Anomaly"].sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "IQR Anomalies",
            f"{int(iqr_count):,}"
        )

    with col2:
        st.metric(
            "Isolation Forest Anomalies",
            f"{int(isolation_count):,}"
        )

    with col3:
        st.metric(
            "Z-Score Anomalies",
            f"{int(zscore_count):,}"
        )

    # =========================
    # ANOMALY DETECTION CHART
    #  =========================

    st.subheader("Anomaly Detection Overview")

    st.caption(
    "Comparison of detected anomalies across the three detection techniques."
    )

    anomaly_chart_df = pd.DataFrame({
    "Detection Method": [
        "IQR",
        "Isolation Forest",
        "Z-Score"
    ],
    "Anomalies": [
        int(iqr_count),
        int(isolation_count),
        int(zscore_count)
    ]
    })

    # Interactive anomaly detection comparison chart
    fig = go.Figure()

    fig.add_trace(
    go.Bar(
        x=anomaly_chart_df["Detection Method"],
        y=anomaly_chart_df["Anomalies"],
        text=anomaly_chart_df["Anomalies"],
        textposition="auto",
        name="Detected Anomalies"
    )
    )

    fig.update_layout(
    height=450,
    xaxis_title="Detection Method",
    yaxis_title="Number of Anomalies",
    hovermode="x",
    showlegend=False,
    margin=dict(l=20, r=20, t=30, b=20)
    )

    st.plotly_chart(
    fig,
    use_container_width=True
    )
    
    st.subheader("Anomaly Detection Data")
    st.caption(
    "Showing the first 100 anomaly records based on the currently selected filters."
)

    st.dataframe(
        filtered_anomaly_df.head(100),
        use_container_width=True
    )

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

    # Validate forecast output
    forecast_days = len(forecast_df)

    if forecast_days == 90:
        st.success("90-day forecast loaded successfully.")
    else:
        st.warning(
            f"Expected 90 forecast days, but found {forecast_days}."
        )

    # =========================
    # STANDARD FORECAST
    # =========================

    st.subheader("Forecast Data")

    st.caption(
        "Showing the available 90-day demand forecast generated by the forecasting model."
    )

    st.dataframe(
        forecast_df,
        use_container_width=True
    )

    # =========================
    # 90-DAY FORECAST CHART
    # =========================

    st.subheader("90-Day Demand Forecast Trend")

    st.caption(
    "Interactive view of predicted demand across the 90-day forecast period."
    )

    forecast_chart_df = (
    forecast_df[
        ["Date", "Forecast"]
    ]
    .set_index("Date")
    .sort_index()
)

    st.line_chart(
    forecast_chart_df["Forecast"],
        use_container_width=True
    )

    # =========================
    # HISTORICAL + FORECAST COMPARISON
    # =========================

    st.subheader("Historical vs Forecast Demand")

    st.caption(
    "Comparison of recent historical demand with the upcoming 90-day forecast."
    )

    # Prepare historical daily demand
    comparison_historical = (
    df.groupby("Date", as_index=False)["Units Sold"]
    .sum()
    .sort_values("Date")
    )

    # Take the most recent 30 historical days
    comparison_historical = comparison_historical.tail(30)

    # Rename for comparison
    comparison_historical = comparison_historical.rename(
    columns={"Units Sold": "Historical Demand"}
    )

    # Prepare forecast data
    comparison_forecast = forecast_df[
    ["Date", "Forecast"]
    ].copy()

    comparison_forecast = comparison_forecast.rename(
    columns={"Forecast": "Forecast Demand"}
    )

    # Combine historical and forecast data
    comparison_df = pd.concat(
    [
        comparison_historical.set_index("Date"),
        comparison_forecast.set_index("Date")
    ],
    axis=1
    ).sort_index()

    # Interactive Historical vs Forecast comparison chart
    fig = go.Figure()

    # Historical Demand
    fig.add_trace(
    go.Scatter(
        x=comparison_historical["Date"],
        y=comparison_historical["Historical Demand"],
        mode="lines+markers",
        name="Historical Demand",
        line=dict(width=2),
        marker=dict(size=5),
        hovertemplate=
            "<b>Historical Demand</b><br>"
            "Date: %{x|%d %b %Y}<br>"
            "Demand: %{y:,.0f}<extra></extra>"
        )
    )

    # Forecast Demand
    fig.add_trace(
    go.Scatter(
        x=comparison_forecast["Date"],
        y=comparison_forecast["Forecast Demand"],
        mode="lines+markers",
        name="Forecast Demand",
        line=dict(width=2, dash="dash"),
        marker=dict(size=5),
        hovertemplate=
            "<b>Forecast Demand</b><br>"
            "Date: %{x|%d %b %Y}<br>"
            "Demand: %{y:,.0f}<extra></extra>"
        )
        )

    fig.update_layout(
    height=500,
    xaxis_title="Date",
    yaxis_title="Demand (Units)",
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    margin=dict(l=20, r=20, t=50, b=20)
    )

    fig.update_xaxes(
    rangeslider_visible=True
    )

    st.plotly_chart(
    fig,
    use_container_width=True
    )

    st.subheader("Forecast Summary")

    col1, col2, col3, col4, col5 = st.columns(5, gap="medium")

    with col1:
        st.metric(
            "Forecast Records",
            f"{len(forecast_df):,}"
        )

    with col2:
        st.metric(
            "Total Forecast",
            f"{forecast_df['Forecast'].sum():,.2f}"
        )

    with col3:
        st.metric(
            "Average Forecast",
            f"{forecast_df['Forecast'].mean():,.2f}"
        )

    with col4:
        st.metric(
            "Maximum Forecast",
            f"{forecast_df['Forecast'].max():,.2f}"
        )

    with col5:
        st.metric(
            "Minimum Forecast",
            f"{forecast_df['Forecast'].min():,.2f}"
        )   

    # =========================
    # BUSINESS INSIGHTS
    # =========================

    st.subheader("Key Business Insights")

    # Calculate anomaly rate
    anomaly_rate = (
        anomaly_count / len(filtered_df) * 100
        if len(filtered_df) > 0
        else 0
    )

    # Recent 30-day historical demand
    recent_historical = (
    filtered_df
    .groupby("Date")["Units Sold"]
    .sum()
    .sort_index()
    .tail(30)
    .mean()
    if not filtered_df.empty
    else 0
    )

    # Average forecast
    avg_forecast = forecast_df["Forecast"].mean()

    # Forecast change compared with recent historical demand
    forecast_change = (
        ((avg_forecast - recent_historical) / recent_historical) * 100
        if recent_historical > 0
        else 0
    )

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown(
            f"""
            <div class="feature-card">
                <h4>Demand Outlook</h4>
                <p>
                The average forecast demand is
                <b>{avg_forecast:,.0f}</b> units per day
                across the 90-day forecast period.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="feature-card">
                <h4>Demand Change</h4>
                <p>
                The forecast indicates a
                <b>{abs(forecast_change):.1f}%</b>
                {"increase" if forecast_change >= 0 else "decrease"}
                compared with the recent 30-day average demand.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="feature-card">
                <h4>Anomaly Risk</h4>
                <p>
                Approximately <b>{anomaly_rate:.2f}%</b>
                of the filtered historical records are
                identified as anomalies.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.info(
        "Business Insight: Use the forecast trend for inventory planning, "
        "monitor detected anomalies for unusual demand behavior, and "
        "compare historical demand with forecast demand to support "
        "future supply chain decisions."
    )

    # =========================
    # ADVANCED ARIMA FORECAST
    # =========================

    st.subheader("Advanced ARIMA Forecast")

    st.markdown("""
    <div class="home-card">

    <h3>ARIMA-Based Demand Forecast</h3>

    <p>
    The ARIMA model provides advanced demand predictions by analyzing
    historical demand patterns and time-series behavior.
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.caption(
        "ARIMA model performance is summarized below using actual demand "
        "and predicted demand values."
    )

    st.subheader("ARIMA Forecast Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "ARIMA Records",
            f"{len(advanced_forecast_df):,}"
        )

    with col2:
        st.metric(
            "Average Actual",
            f"{advanced_forecast_df['Actual'].mean():,.2f}"
        )

    with col3:
        st.metric(
            "Average ARIMA Prediction",
            f"{advanced_forecast_df['ARIMA_Prediction'].mean():,.2f}"
        )

    with col4:
        arima_difference = (
            advanced_forecast_df["ARIMA_Prediction"].mean()
            - advanced_forecast_df["Actual"].mean()
        )

        st.metric(
            "Average Difference",
            f"{arima_difference:,.2f}"
        )
        
    # =========================
    # ACTUAL VS ARIMA PREDICTION
    # =========================

    st.subheader("Actual vs ARIMA Prediction")

    st.caption(
        "Comparison of actual demand with ARIMA model predictions."
    )

    fig = go.Figure()

    # Actual Demand
    fig.add_trace(
        go.Scatter(
            x=advanced_forecast_df["Date"],
            y=advanced_forecast_df["Actual"],
            mode="lines",
            name="Actual Demand",
            line=dict(width=2)
        )
    )

    # ARIMA Prediction
    fig.add_trace(
        go.Scatter(
            x=advanced_forecast_df["Date"],
            y=advanced_forecast_df["ARIMA_Prediction"],
            mode="lines",
            name="ARIMA Prediction",
            line=dict(width=2, dash="dash")
        )
    )

    fig.update_layout(
        height=500,
        xaxis_title="Date",
        yaxis_title="Demand (Units)",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )