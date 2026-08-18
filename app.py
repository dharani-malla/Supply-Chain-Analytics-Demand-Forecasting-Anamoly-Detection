import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# ==========================================
# PAGE CONFIGURATIONS & THEME INTEGRATION
# ==========================================
st.set_page_config(
    page_title="Supply Chain Analytics Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS Injection
st.markdown("""
<style>
    /* Global Application Styles */
    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }
    
    /* Headings styling */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 700 !important;
        margin-top: 10px !important;
        margin-bottom: 10px !important;
    }

    /* Sidebar Panel Background */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    
    /* Hide Radio standard circle indicators (markers) in all Streamlit versions */
    div[data-testid="stRadio"] div[role="radiogroup"] label div[role="presentation"],
    div[data-testid="stRadio"] div[role="radiogroup"] label div[data-testid="stMarker"],
    div[data-testid="stRadio"] div[role="radiogroup"] label [class*="RadioCircle"],
    div[data-testid="stRadio"] div[role="radiogroup"] label input[type="radio"] {
        display: none !important;
    }
    
    /* Navigation Radio Items wrapper */
    div[data-testid="stRadio"] div[role="radiogroup"] {
        gap: 6px !important;
        padding: 0 !important;
    }
    
    /* Navigation Radio Option label */
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        padding: 10px 14px !important;
        border-radius: 8px !important;
        background-color: transparent !important;
        border: 1px solid transparent !important;
        transition: all 0.2s ease-in-out !important;
        cursor: pointer !important;
        margin-bottom: 4px !important;
        display: block !important;
        width: 100% !important;
    }
    
    /* High-contrast white for inactive navigation text */
    div[data-testid="stRadio"] div[role="radiogroup"] label * {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 14.5px !important;
        background-color: transparent !important;
    }
    
    /* Hover state styling */
    div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
        background-color: #1e293b !important;
        border-color: #334155 !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label:hover * {
        color: #ffffff !important;
    }
    
    /* Bright blue accent for active/selected navigation text */
    div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
        background-color: #1e293b !important;
        border-color: #334155 !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) * {
        color: #38bdf8 !important;
        font-weight: 700 !important;
    }
    
    /* Fallback selector for selected text (using sibling selectors) */
    div[data-testid="stRadio"] div[role="radiogroup"] label input:checked ~ * {
        color: #38bdf8 !important;
        font-weight: 700 !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label input:checked + div * {
        color: #38bdf8 !important;
        font-weight: 700 !important;
    }
    
    /* Custom divider line */
    .sidebar-divider {
        margin: 15px 0;
        border-bottom: 1px solid #1e293b;
    }
    
    /* High-contrast white for FILTERS heading */
    .filter-section-header {
        font-size: 11px;
        font-weight: 800 !important;
        color: #ffffff !important;
        letter-spacing: 1.5px;
        margin: 15px 0 10px 0;
        text-transform: uppercase;
    }
    
    /* High-contrast white for Sidebar labels */
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
        font-weight: bold !important;
    }
    
    /* Make selectbox selected values & placeholders white */
    section[data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #ffffff !important;
    }
    
    /* Custom Business Insights cards */
    .insight-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 18px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.03);
        border: 1px solid #e2e8f0;
    }
    
    .insight-card h4 {
        color: #0f172a !important;
        margin-top: 0 !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .insight-card p {
        color: #334155;
        font-size: 14.5px;
        line-height: 1.7;
        margin-bottom: 0;
    }
    
    /* Info box overrides */
    div[data-testid="stInfo"] {
        background-color: #1e3a5f !important;
        color: #e0f2fe !important;
        border: 1px solid #0369a1 !important;
        border-radius: 8px;
    }

    /* Warning box overrides */
    div[data-testid="stWarning"] {
        background-color: #451a03 !important;
        color: #fef3c7 !important;
        border: 1px solid #b45309 !important;
        border-radius: 8px;
    }
    
    /* Success box overrides */
    div[data-testid="stSuccess"] {
        background-color: #064e3b !important;
        color: #d1fae5 !important;
        border: 1px solid #047857 !important;
        border-radius: 8px;
    }
    
    /* Error box overrides */
    div[data-testid="stError"] {
        background-color: #450a0a !important;
        color: #fecaca !important;
        border: 1px solid #991b1b !important;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to render modern KPI cards
def render_kpi_card(title, value, description, icon, accent_color="#2563eb"):
    st.markdown(f"""
    <div style="
        background-color: #ffffff;
        border-left: 5px solid {accent_color};
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border-top: 1px solid #e2e8f0;
        border-right: 1px solid #e2e8f0;
        border-bottom: 1px solid #e2e8f0;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-size: 12px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;">{title}</span>
            <span style="font-size: 22px; color: {accent_color};">{icon}</span>
        </div>
        <div style="font-size: 26px; font-weight: 800; color: #0f172a; line-height: 1.2; margin-bottom: 4px;">{value}</div>
        <div style="font-size: 12px; color: #64748b; font-weight: 500;">{description}</div>
    </div>
    """, unsafe_allow_html=True)

# Helper function to apply dark navy Plotly theme layouts
def apply_plotly_theme(fig, title, x_title, y_title):
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16, family="Segoe UI, sans-serif", color="#ffffff"),
            x=0,
            y=0.96
        ),
        xaxis=dict(
            title=dict(
                text=x_title,
                font=dict(size=12, color="#94a3b8")
            ),
            tickfont=dict(size=11, color="#cbd5e1"),
            gridcolor="#1e293b",
            showgrid=True
        ),
        yaxis=dict(
            title=dict(
                text=y_title,
                font=dict(size=12, color="#94a3b8")
            ),
            tickfont=dict(size=11, color="#cbd5e1"),
            gridcolor="#1e293b",
            showgrid=True
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
        margin=dict(l=10, r=10, t=55, b=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color="#cbd5e1")
        )
    )

# Safe MAPE calculation helper
def calculate_mape(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    mask = y_true != 0
    if not np.any(mask):
        return 0.0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

# ==========================================
# DATA LOADING (WITH @st.cache_data)
# ==========================================
@st.cache_data
def load_data():
    try:
        # Load historical + anomaly dataset
        hist_path = "data/final_anomaly_dataset (1).xlsx"
        if not os.path.exists(hist_path):
            st.error(f"❌ Missing file in workspace: {hist_path}. Please check data folder structure.")
            st.stop()
        historical_df = pd.read_excel(hist_path)
        historical_df["Date"] = pd.to_datetime(historical_df["Date"])
        
        # Load forecast dataset
        forecast_path = "data/future_forecast.xlsx"
        if not os.path.exists(forecast_path):
            st.error(f"❌ Missing file in workspace: {forecast_path}. Please check data folder structure.")
            st.stop()
        forecast_df = pd.read_excel(forecast_path)
        forecast_df["Date"] = pd.to_datetime(forecast_df["Date"])
        forecast_df["Forecast"] = pd.to_numeric(forecast_df["Forecast"], errors="coerce")
        forecast_df = forecast_df.dropna(subset=["Date", "Forecast"]).sort_values("Date")
        forecast_df["Forecast"] = forecast_df["Forecast"].round(2)
        
        # Load advanced ARIMA forecast
        advanced_path = "data/advanced_forecast.xlsx"
        if not os.path.exists(advanced_path):
            st.error(f"❌ Missing file in workspace: {advanced_path}. Please check data folder structure.")
            st.stop()
        advanced_forecast_df = pd.read_excel(advanced_path)
        advanced_forecast_df["Date"] = pd.to_datetime(advanced_forecast_df["Date"])
        advanced_forecast_df["Actual"] = pd.to_numeric(advanced_forecast_df["Actual"], errors="coerce")
        advanced_forecast_df["ARIMA_Prediction"] = pd.to_numeric(advanced_forecast_df["ARIMA_Prediction"], errors="coerce")
        advanced_forecast_df = advanced_forecast_df.dropna(subset=["Date", "Actual", "ARIMA_Prediction"]).sort_values("Date")
        advanced_forecast_df["ARIMA_Prediction"] = advanced_forecast_df["ARIMA_Prediction"].round(2)
        
        return historical_df, forecast_df, advanced_forecast_df
    except Exception as e:
        st.error(f"⚠️ Error reading raw Excel data files: {e}")
        st.stop()

# Retrieve clean datasets
historical_df, forecast_df, advanced_forecast_df = load_data()
df = historical_df.copy()
anomaly_df = historical_df.copy().sort_values("Date")

# ==========================================
# SIDEBAR NAVIGATION & FILTER INTERFACE
# ==========================================
st.sidebar.markdown("""
<div style="padding: 10px 0px; text-align: left;">
    <h2 style="margin: 0; font-size: 20px; font-weight: 800; color: #ffffff; letter-spacing: 0.5px; display: flex; align-items: center; gap: 8px;">
        📦 SUPPLY CHAIN ANALYTICS
    </h2>
    <div style="font-size: 11px; color: #ffffff; font-weight: 600; margin-top: 4px; text-transform: uppercase; letter-spacing: 1px;">
        Demand Forecasting & Anomaly Detection
    </div>
</div>
<div class="sidebar-divider"></div>
""", unsafe_allow_html=True)

# Main navigation Radio choices
selected_page = st.sidebar.radio(
    "NAVIGATION",
    [
        "🏠 Executive Dashboard",
        "📈 Historical Demand",
        "🚨 Anomaly Detection",
        "🔮 Demand Forecast",
        "🤖 ARIMA Forecast"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="filter-section-header">Filters</div>', unsafe_allow_html=True)

# Region filter options selection
region_options = ["All"] + sorted(df["Region"].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("🌍 Region", region_options)

# Category filter options selection
category_options = ["All"] + sorted(df["Category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("📦 Category", category_options)

# Store ID filter options selection
store_options = ["All"] + sorted(df["Store ID"].dropna().unique().tolist())
selected_store = st.sidebar.selectbox("🏪 Store", store_options)

# Compile filtered datasets based on selection
filtered_df = df.copy()
filtered_anomaly_df = anomaly_df.copy()

if selected_region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == selected_region]
    filtered_anomaly_df = filtered_anomaly_df[filtered_anomaly_df["Region"] == selected_region]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]
    filtered_anomaly_df = filtered_anomaly_df[filtered_anomaly_df["Category"] == selected_category]

if selected_store != "All":
    filtered_df = filtered_df[filtered_df["Store ID"] == selected_store]
    filtered_anomaly_df = filtered_anomaly_df[filtered_anomaly_df["Store ID"] == selected_store]

# Validate empty results across filter selections
if filtered_df.empty:
    st.warning("⚠️ No historical demand records matching the selected filters were found.")

if filtered_anomaly_df.empty:
    st.info("ℹ️ No anomaly records matching the selected filters were found.")

# Display a notice on Forecast pages regarding filters scope
if selected_page in ["🔮 Demand Forecast", "🤖 ARIMA Forecast"]:
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.sidebar.caption("ℹ️ Projections represent aggregate system-wide performance and are independent of category/region filters.")

# ==========================================
# PAGE 1: EXECUTIVE DASHBOARD
# ==========================================
if selected_page == "🏠 Executive Dashboard":
    st.markdown("""
    <div style="margin-bottom: 25px;">
        <h1 style="margin: 0; font-size: 32px; font-weight: 800; color: #ffffff;">SUPPLY CHAIN ANALYTICS</h1>
        <div style="font-size: 16px; color: #3b82f6; font-weight: 600; margin-top: 5px;">Demand Forecasting & Anomaly Detection</div>
        <p style="font-size: 14px; color: #94a3b8; margin-top: 10px; line-height: 1.6; max-width: 800px;">
            Monitor historical demand, identify operational anomalies, and forecast future demand to support smarter inventory and supply-chain decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate Executive KPIs
    total_demand_val = filtered_df["Units Sold"].sum() if not filtered_df.empty else 0
    avg_demand_val = filtered_df["Units Sold"].mean() if not filtered_df.empty else 0
    
    # Anomaly count based on active filters
    iqr_flag = filtered_anomaly_df["IQR_Anomaly"] == 1 if "IQR_Anomaly" in filtered_anomaly_df.columns else pd.Series(False, index=filtered_anomaly_df.index)
    if_flag = filtered_anomaly_df["IsolationForest"] == 1 if "IsolationForest" in filtered_anomaly_df.columns else pd.Series(False, index=filtered_anomaly_df.index)
    z_flag = (filtered_anomaly_df["ZScore_Anomaly"] == 1) | (filtered_anomaly_df["ZScore_Anomaly"] == True) if "ZScore_Anomaly" in filtered_anomaly_df.columns else pd.Series(False, index=filtered_anomaly_df.index)
    total_anomalies_val = (iqr_flag | if_flag | z_flag).sum() if not filtered_anomaly_df.empty else 0
    forecast_horizon_val = len(forecast_df)
    
    # Render KPI Cards Grid
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Total Demand", f"{total_demand_val:,.0f}", "Units sold across range", "📦", "#2563eb")
    with col2:
        render_kpi_card("Average Demand", f"{avg_demand_val:,.1f}", "Daily units sold mean", "📊", "#0ea5e9")
    with col3:
        render_kpi_card("Total Anomalies", f"{total_anomalies_val:,}", "Flagged irregular peaks/dips", "🚨", "#ef4444")
    with col4:
        render_kpi_card("Forecast Horizon", f"{forecast_horizon_val} Days", "Future predictions window", "🔮", "#8b5cf6")
        
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    # Section: Demand Overview Chart
    st.markdown("### 📈 Demand Overview")
    if not filtered_df.empty:
        daily_demand_df = filtered_df.groupby("Date", as_index=False)["Units Sold"].sum().sort_values("Date")
        fig_demand = go.Figure()
        fig_demand.add_trace(go.Scatter(
            x=daily_demand_df["Date"],
            y=daily_demand_df["Units Sold"],
            mode="lines",
            name="Units Sold",
            line=dict(color="#2563eb", width=2),
            hovertemplate="Date: %{x|%d %b %Y}<br>Units Sold: %{y:,.0f}<extra></extra>"
        ))
        apply_plotly_theme(fig_demand, "Historical Demand Trend Over Time", "Date", "Units Sold")
        st.plotly_chart(fig_demand, use_container_width=True)
    else:
        st.info("No demand trend to display for selected filters.")
        
    # Two-Column Section: Anomaly & Forecast Overview
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### 🚨 Anomaly Overview")
        if not filtered_anomaly_df.empty and total_anomalies_val > 0:
            iqr_sum = iqr_flag.sum()
            if_sum = if_flag.sum()
            z_sum = z_flag.sum()
            
            fig_anom_overview = go.Figure()
            fig_anom_overview.add_trace(go.Bar(
                x=["IQR Method", "Isolation Forest", "Z-Score"],
                y=[iqr_sum, if_sum, z_sum],
                marker_color=["#ef4444", "#f97316", "#dc2626"],
                text=[int(iqr_sum), int(if_sum), int(z_sum)],
                textposition="auto",
                hovertemplate="Method: %{x}<br>Flagged Outliers: %{y:,}<extra></extra>"
            ))
            apply_plotly_theme(fig_anom_overview, "Anomalies Flagged by Algorithm Detection", "Detection Method", "Count")
            st.plotly_chart(fig_anom_overview, use_container_width=True)
        else:
            st.info("No anomalies recorded under the current filters configuration.")
            
    with col_right:
        st.markdown("### 🔮 Forecast Overview")
        if not forecast_df.empty:
            fig_fc_overview = go.Figure()
            fig_fc_overview.add_trace(go.Scatter(
                x=forecast_df["Date"],
                y=forecast_df["Forecast"],
                mode="lines",
                name="Aggregate Forecast",
                line=dict(color="#8b5cf6", width=2, dash="dash"),
                hovertemplate="Date: %{x|%d %b %Y}<br>Predicted: %{y:,.0f}<extra></extra>"
            ))
            apply_plotly_theme(fig_fc_overview, "90-Day System-Wide Demand Forecast Projections", "Date", "Predicted Units")
            st.plotly_chart(fig_fc_overview, use_container_width=True)
        else:
            st.info("Forecast data unavailable.")

    # Section: Key Business Insights
    st.markdown("### 💡 KEY BUSINESS INSIGHTS")
    col_ins1, col_ins2, col_ins3 = st.columns(3)
    
    with col_ins1:
        if not filtered_df.empty:
            daily_grouped = filtered_df.groupby("Date")["Units Sold"].sum()
            max_date = daily_grouped.idxmax()
            max_val = daily_grouped.max()
            min_date = daily_grouped.idxmin()
            min_val = daily_grouped.min()
            
            st.markdown(f"""
            <div class="insight-card">
                <h4>📈 Peak & Trough Demand</h4>
                <p>
                    The highest demand occurred on <b>{max_date.strftime('%d %b %Y')}</b> with a total volume of <b>{max_val:,.0f} units</b>.<br>
                    The lowest demand period was recorded on <b>{min_date.strftime('%d %b %Y')}</b> with <b>{min_val:,.0f} units</b>.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="insight-card">
                <h4>📈 Peak & Trough Demand</h4>
                <p>No historical records are available to analyze peak volumes.</p>
            </div>
            """, unsafe_allow_html=True)
            
    with col_ins2:
        if not filtered_df.empty:
            anomaly_rate = (total_anomalies_val / len(filtered_df)) * 100
            st.markdown(f"""
            <div class="insight-card">
                <h4>🚨 Operational Anomaly Audit</h4>
                <p>
                    Out of <b>{len(filtered_df):,}</b> total logged observations, 
                    <b>{total_anomalies_val:,}</b> anomalies were detected, representing an anomaly rate of <b>{anomaly_rate:.2f}%</b>.<br>
                    These demand spikes or dips warrant active supply chain inspection.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="insight-card">
                <h4>🚨 Operational Anomaly Audit</h4>
                <p>No anomaly records are available for audit calculations.</p>
            </div>
            """, unsafe_allow_html=True)
            
    with col_ins3:
        if not forecast_df.empty and not filtered_df.empty:
            recent_30_mean = filtered_df.groupby("Date")["Units Sold"].sum().tail(30).mean()
            fc_mean = forecast_df["Forecast"].mean()
            trend_pct = ((fc_mean - recent_30_mean) / recent_30_mean) * 100 if recent_30_mean > 0 else 0
            trend_desc = "increase" if trend_pct >= 0 else "decrease"
            
            st.markdown(f"""
            <div class="insight-card">
                <h4>🔮 Forward Predictive Trend</h4>
                <p>
                    The aggregate 90-day forecast projects an average demand of <b>{fc_mean:,.1f} units/day</b>.<br>
                    This represents a <b>{abs(trend_pct):.1f}% {trend_desc}</b> compared to the average of the last 30 historical sales records.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="insight-card">
                <h4>🔮 Forward Predictive Trend</h4>
                <p>Forecast trend calculations are unavailable due to insufficient datasets.</p>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# PAGE 2: HISTORICAL DEMAND
# ==========================================
elif selected_page == "📈 Historical Demand":
    st.markdown("""
    <div style="margin-bottom: 25px;">
        <h1 style="margin: 0; font-size: 32px; font-weight: 800; color: #ffffff;">📈 Historical Demand Analysis</h1>
        <div class="subtitle">Analyze historical demand patterns across time, region, category, and store.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate historical KPIs
    total_records = len(filtered_df)
    total_demand = filtered_df["Units Sold"].sum() if not filtered_df.empty else 0
    avg_demand = filtered_df["Units Sold"].mean() if not filtered_df.empty else 0
    peak_demand = filtered_df["Units Sold"].max() if not filtered_df.empty else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Total Records", f"{total_records:,}", "Total raw log observations", "📋", "#3b82f6")
    with col2:
        render_kpi_card("Total Demand", f"{total_demand:,.0f}", "Units sold across scope", "📦", "#2563eb")
    with col3:
        render_kpi_card("Average Demand", f"{avg_demand:,.1f}", "Average sales units/day", "📊", "#0ea5e9")
    with col4:
        render_kpi_card("Peak Demand", f"{peak_demand:,.0f}", "Max single daily observation", "📈", "#10b981")
        
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    # Main Trend Chart
    st.markdown("### Historical Demand Trend")
    if not filtered_df.empty:
        daily_trend_df = filtered_df.groupby("Date", as_index=False)["Units Sold"].sum().sort_values("Date")
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=daily_trend_df["Date"],
            y=daily_trend_df["Units Sold"],
            mode="lines",
            name="Daily Demand",
            line=dict(color="#2563eb", width=2),
            hovertemplate="Date: %{x|%d %b %Y}<br>Units Sold: %{y:,.0f}<extra></extra>"
        ))
        apply_plotly_theme(fig_trend, "Daily Total Demand Trend (Units Sold)", "Date", "Units Sold")
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("No data available to display trend.")
        
    # Two Columns: Regions & Categories distribution
    col_r, col_c = st.columns(2)
    
    with col_r:
        st.markdown("### Demand by Region")
        if not filtered_df.empty and "Region" in filtered_df.columns:
            region_df = filtered_df.groupby("Region", as_index=False)["Units Sold"].sum().sort_values("Units Sold", ascending=False)
            fig_region = go.Figure()
            fig_region.add_trace(go.Bar(
                x=region_df["Region"],
                y=region_df["Units Sold"],
                marker_color="#2563eb",
                text=region_df["Units Sold"].apply(lambda val: f"{val:,.0f}"),
                textposition="auto",
                hovertemplate="Region: %{x}<br>Units Sold: %{y:,.0f}<extra></extra>"
            ))
            apply_plotly_theme(fig_region, "Demand Distribution by Geographic Region", "Region", "Units Sold")
            st.plotly_chart(fig_region, use_container_width=True)
        else:
            st.info("Region column unavailable in dataset.")
            
    with col_c:
        st.markdown("### Demand by Category")
        if not filtered_df.empty and "Category" in filtered_df.columns:
            cat_df = filtered_df.groupby("Category", as_index=False)["Units Sold"].sum().sort_values("Units Sold", ascending=True)
            fig_cat = go.Figure()
            fig_cat.add_trace(go.Bar(
                y=cat_df["Category"],
                x=cat_df["Units Sold"],
                orientation="h",
                marker_color="#0ea5e9",
                text=cat_df["Units Sold"].apply(lambda val: f"{val:,.0f}"),
                textposition="auto",
                hovertemplate="Category: %{y}<br>Units Sold: %{x:,.0f}<extra></extra>"
            ))
            apply_plotly_theme(fig_cat, "Demand Distribution by Product Category", "Units Sold", "Category")
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.info("Category column unavailable in dataset.")
            
    # Section: Summary Table
    st.markdown("### Demand Summary")
    if not filtered_df.empty:
        st.caption("Showing descriptive summary statistics for Units Sold under active filters.")
        summary_stats = filtered_df["Units Sold"].describe().to_frame().reset_index()
        summary_stats.columns = ["Metric", "Value"]
        # Format metrics beautifully
        def format_summary(row):
            if row["Metric"] in ["count"]:
                return f"{int(row['Value']):,}"
            else:
                return f"{row['Value']:,.2f}"
        summary_stats["Value"] = summary_stats.apply(format_summary, axis=1)
        st.dataframe(summary_stats, use_container_width=True)
        
        # Historical Insights
        peak_date = filtered_df.loc[filtered_df["Units Sold"].idxmax(), "Date"].strftime('%d %b %Y')
        avg_units = filtered_df["Units Sold"].mean()
        
        region_text = ""
        if "Region" in filtered_df.columns and len(filtered_df["Region"].unique()) > 1:
            top_reg = filtered_df.groupby("Region")["Units Sold"].sum().idxmax()
            region_text = f"<li><b>Geographic Leader:</b> The primary driver of sales volume geographically is the <b>{top_reg}</b> region.</li>"
            
        cat_text = ""
        if "Category" in filtered_df.columns and len(filtered_df["Category"].unique()) > 1:
            top_cat = filtered_df.groupby("Category")["Units Sold"].sum().idxmax()
            cat_text = f"<li><b>Category Driver:</b> Product inventory requirements are heavily influenced by the <b>{top_cat}</b> category.</li>"
            
        st.markdown(f"""
        <div class="insight-card">
            <h4 style="color: #2563eb !important; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; margin-bottom: 12px;">💡 Historical Demand Insights</h4>
            <ul style="color: #475569; font-size: 14.5px; line-height: 1.8; margin-top: 10px; margin-bottom: 0; padding-left: 20px;">
                <li><b>Volume Highlights:</b> Demand patterns show a daily sales average of <b>{avg_units:,.1f} units</b>, peaking at <b>{peak_demand:,.0f} units</b> on <b>{peak_date}</b>.</li>
                {region_text}
                {cat_text}
                <li><b>Supply Strategy:</b> Logistics plans should be structured to support these core volume trends and allocate buffer inventory dynamically.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No demand insights available for empty records selection.")

# ==========================================
# PAGE 3: ANOMALY DETECTION
# ==========================================
elif selected_page == "🚨 Anomaly Detection":
    st.markdown("""
    <div style="margin-bottom: 25px;">
        <h1 style="margin: 0; font-size: 32px; font-weight: 800; color: #ffffff;">🚨 Anomaly Detection</h1>
        <div class="subtitle">Identify unusual demand patterns that may indicate operational issues.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate anomaly flags
    total_anom_records = len(filtered_anomaly_df)
    
    iqr_anoms = filtered_anomaly_df["IQR_Anomaly"] == 1 if "IQR_Anomaly" in filtered_anomaly_df.columns else pd.Series(False, index=filtered_anomaly_df.index)
    if_anoms = filtered_anomaly_df["IsolationForest"] == 1 if "IsolationForest" in filtered_anomaly_df.columns else pd.Series(False, index=filtered_anomaly_df.index)
    z_anoms = (filtered_anomaly_df["ZScore_Anomaly"] == 1) | (filtered_anomaly_df["ZScore_Anomaly"] == True) if "ZScore_Anomaly" in filtered_anomaly_df.columns else pd.Series(False, index=filtered_anomaly_df.index)
    
    # Consolidated anomaly flag
    is_anomaly = iqr_anoms | if_anoms | z_anoms
    
    anomaly_count = is_anomaly.sum()
    normal_count = total_anom_records - anomaly_count
    anomaly_rate = (anomaly_count / total_anom_records) * 100 if total_anom_records > 0 else 0
    
    # KPI Grid
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Total Records", f"{total_anom_records:,}", "Total data observations", "📋", "#3b82f6")
    with col2:
        render_kpi_card("Normal Records", f"{normal_count:,}", "Consistent sales cycles", "✅", "#10b981") # Green
    with col3:
        render_kpi_card("Anomalies", f"{anomaly_count:,}", "Outliers flagged by algorithms", "🚨", "#ef4444") # Red
    with col4:
        render_kpi_card("Anomaly Rate", f"{anomaly_rate:.2f}%", "Outlier share of observations", "📈", "#f59e0b") # Orange
        
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    # Main Anomaly Scatter Plot
    st.markdown("### 📊 Demand Anomalies Over Time")
    if not filtered_anomaly_df.empty:
        fig_anom_plot = go.Figure()
        
        # Plot base line
        fig_anom_plot.add_trace(go.Scatter(
            x=filtered_anomaly_df["Date"],
            y=filtered_anomaly_df["Units Sold"],
            mode="lines",
            name="Demand Volume",
            line=dict(color="#2563eb", width=2),
            hovertemplate="Date: %{x|%d %b %Y}<br>Units Sold: %{y:,.0f}<extra></extra>"
        ))
        
        # Add highlighted anomalies
        anom_subset = filtered_anomaly_df[is_anomaly]
        fig_anom_plot.add_trace(go.Scatter(
            x=anom_subset["Date"],
            y=anom_subset["Units Sold"],
            mode="markers",
            name="Flagged Anomaly",
            marker=dict(color="#ef4444", size=9, symbol="circle-x", line=dict(color="#ffffff", width=1)),
            hovertemplate="<b>Anomaly Outlier</b><br>Date: %{x|%d %b %Y}<br>Units Sold: %{y:,.0f}<extra></extra>"
        ))
        
        apply_plotly_theme(fig_anom_plot, "Historical Demand with Highlighted Anomalies", "Date", "Units Sold")
        st.plotly_chart(fig_anom_plot, use_container_width=True)
    else:
        st.info("No anomaly dataset to plot.")
        
    # Two Columns: Anomaly distribution & trend over time
    col_dist, col_tr = st.columns(2)
    
    with col_dist:
        st.markdown("### Anomaly Distribution")
        if not filtered_anomaly_df.empty:
            iqr_sum = iqr_anoms.sum()
            if_sum = if_anoms.sum()
            z_sum = z_anoms.sum()
            
            fig_dist = go.Figure()
            fig_dist.add_trace(go.Bar(
                x=["IQR Method", "Isolation Forest", "Z-Score"],
                y=[iqr_sum, if_sum, z_sum],
                marker_color=["#ef4444", "#f59e0b", "#dc2626"],
                text=[int(iqr_sum), int(if_sum), int(z_sum)],
                textposition="auto",
                hovertemplate="Method: %{x}<br>Flagged Anomalies: %{y:,}<extra></extra>"
            ))
            apply_plotly_theme(fig_dist, "Count of Outliers Flagged by Detection Method", "Method", "Count")
            st.plotly_chart(fig_dist, use_container_width=True)
        else:
            st.info("Anomaly count data is empty.")
            
    with col_tr:
        st.markdown("### Anomaly Trend")
        if not filtered_anomaly_df.empty:
            # Group anomalies by Month to see trend
            anom_trend = filtered_anomaly_df.copy()
            anom_trend["Is_Anomaly"] = is_anomaly.astype(int)
            monthly_anom = anom_trend.groupby(anom_trend["Date"].dt.to_period("M"))["Is_Anomaly"].sum().reset_index()
            monthly_anom["Date"] = monthly_anom["Date"].dt.to_timestamp()
            
            fig_tr = go.Figure()
            fig_tr.add_trace(go.Scatter(
                x=monthly_anom["Date"],
                y=monthly_anom["Is_Anomaly"],
                mode="lines+markers",
                name="Monthly Anomalies",
                line=dict(color="#ef4444", width=2),
                marker=dict(color="#ef4444", size=6),
                hovertemplate="Month: %{x|%b %Y}<br>Anomalies: %{y}<extra></extra>"
            ))
            apply_plotly_theme(fig_tr, "Monthly Occurrence of Flagged Anomalies", "Date", "Anomalies Count")
            st.plotly_chart(fig_tr, use_container_width=True)
        else:
            st.info("No historical trends to show.")
            
    # Section: Anomaly Table and Explanation
    st.markdown("### 🔎 Anomaly Summary")
    if not filtered_anomaly_df.empty:
        anom_only_df = filtered_anomaly_df[is_anomaly].sort_values("Date", ascending=False)
        if not anom_only_df.empty:
            st.caption("Displaying up to the first 100 anomaly records detected in logs.")
            
            # Form clean display columns
            display_cols = ["Date", "Store ID", "Product ID", "Category", "Region", "Units Sold", "Inventory Level"]
            available_cols = [col for col in display_cols if col in anom_only_df.columns]
            
            st.dataframe(anom_only_df[available_cols].head(100), use_container_width=True)
        else:
            st.success("✅ Clean operations audit: Zero anomaly records were flagged under the current configuration.")
            
        st.markdown("""
        <div class="insight-card" style="border-top: 4px solid #ef4444;">
            <h4 style="color: #ef4444 !important; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; margin-bottom: 12px;">🔎 Operations & Supply Anomaly Impact</h4>
            <p style="color: #334155; font-size: 14.5px; line-height: 1.7; margin-bottom: 12px;">
                Anomalies represent demand observations that deviate significantly from expected patterns and may require operational investigation.
            </p>
            <ul style="color: #475569; font-size: 14px; line-height: 1.8; padding-left: 20px; margin-bottom: 0;">
                <li><b>Spike Triggers:</b> Sudden bulk corporate orders, seasonal shopping surges, or active marketing promotions.</li>
                <li><b>Drop Triggers:</b> Inventory stockouts, supplier delivery failures, system logging errors, or severe weather disruptions.</li>
                <li><b>Inventory Risk:</b> Spikes risk stock depletion and customer dissatisfaction, while dips can lead to warehouse overstocking.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# PAGE 4: DEMAND FORECAST
# ==========================================
elif selected_page == "🔮 Demand Forecast":
    st.markdown("""
    <div style="margin-bottom: 25px;">
        <h1 style="margin: 0; font-size: 32px; font-weight: 800; color: #ffffff;">🔮 90-Day Demand Forecast</h1>
        <div class="subtitle">Explore expected future demand to support inventory and procurement planning.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate Forecast KPIs
    fc_horizon = len(forecast_df)
    fc_avg = forecast_df["Forecast"].mean() if not forecast_df.empty else 0
    fc_max = forecast_df["Forecast"].max() if not forecast_df.empty else 0
    fc_min = forecast_df["Forecast"].min() if not forecast_df.empty else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Forecast Horizon", f"{fc_horizon} Days", "Predictions range length", "🔮", "#8b5cf6")
    with col2:
        render_kpi_card("Average Forecast", f"{fc_avg:,.1f}", "Average expected units/day", "📊", "#3b82f6")
    with col3:
        render_kpi_card("Max Forecast", f"{fc_max:,.1f}", "Peak daily demand expected", "📈", "#10b981")
    with col4:
        render_kpi_card("Min Forecast", f"{fc_min:,.1f}", "Lowest daily demand expected", "📉", "#f59e0b")
        
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    # Main Comparison Chart: Historical vs Future Demand
    st.markdown("### 📈 Historical vs Future Demand")
    if not forecast_df.empty and not historical_df.empty:
        # Aggregate daily historical demand (overall system level)
        hist_daily = historical_df.groupby("Date", as_index=False)["Units Sold"].sum().sort_values("Date")
        
        # Take the most recent 30 days of actual demand to prevent visual clutter
        recent_hist = hist_daily.tail(30)
        
        fig_fc_comp = go.Figure()
        
        # Historical actual trace
        fig_fc_comp.add_trace(go.Scatter(
            x=recent_hist["Date"],
            y=recent_hist["Units Sold"],
            mode="lines+markers",
            name="Historical Demand (Last 30 Days)",
            line=dict(color="#2563eb", width=2),
            marker=dict(size=4),
            hovertemplate="Historical Date: %{x|%d %b %Y}<br>Units Sold: %{y:,.0f}<extra></extra>"
        ))
        
        # Forecast trace
        fig_fc_comp.add_trace(go.Scatter(
            x=forecast_df["Date"],
            y=forecast_df["Forecast"],
            mode="lines+markers",
            name="Future Forecast (Next 90 Days)",
            line=dict(color="#8b5cf6", width=2.5, dash="dash"),
            marker=dict(size=4),
            hovertemplate="Forecast Date: %{x|%d %b %Y}<br>Forecast: %{y:,.0f}<extra></extra>"
        ))
        
        apply_plotly_theme(fig_fc_comp, "Chronological Demand Flow: Historical Actuals to Predictive Projections", "Date", "Demand (Units)")
        st.plotly_chart(fig_fc_comp, use_container_width=True)
    else:
        st.info("Demand history or forecast records missing.")
        
    # Table Section: 90-Day Forecast
    st.markdown("### 📅 90-Day Forecast")
    if not forecast_df.empty:
        st.caption("Detailed daily demand forecast table.")
        # Render clean formatting
        display_fc_df = forecast_df.copy()
        display_fc_df["Forecast"] = display_fc_df["Forecast"].apply(lambda v: f"{v:,.2f}")
        st.dataframe(display_fc_df, use_container_width=True)
        
    # Section: Forecast Insights
    st.markdown("### 💡 Forecast Insights")
    if not forecast_df.empty:
        max_fc_row = forecast_df.loc[forecast_df["Forecast"].idxmax()]
        min_fc_row = forecast_df.loc[forecast_df["Forecast"].idxmin()]
        
        # Assess trend direction (First 15 days average vs last 15 days average)
        first_15 = forecast_df.head(15)["Forecast"].mean()
        last_15 = forecast_df.tail(15)["Forecast"].mean()
        trend_direction = "Increasing Trend 📈" if last_15 > first_15 else "Decreasing Trend 📉"
        trend_detail = f"The forecast projects a daily average of {first_15:,.1f} units initially, shifting towards {last_15:,.1f} units by the end of the 90-day window."
        
        st.markdown(f"""
        <div class="insight-card" style="border-top: 4px solid #8b5cf6;">
            <h4 style="color: #8b5cf6 !important; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; margin-bottom: 12px;">💡 Predictive Demand Forecast Analytics</h4>
            <ul style="color: #475569; font-size: 14.5px; line-height: 1.8; padding-left: 20px; margin-bottom: 0;">
                <li><b>Peak demand projection:</b> Expected on <b>{max_fc_row['Date'].strftime('%d %b %Y')}</b> reaching a maximum of <b>{max_fc_row['Forecast']:,.0f} units</b>.</li>
                <li><b>Minimum demand projection:</b> Expected on <b>{min_fc_row['Date'].strftime('%d %b %Y')}</b> dropping to <b>{min_fc_row['Forecast']:,.0f} units</b>.</li>
                <li><b>Expected Forecast Trend:</b> <b>{trend_direction}</b>. {trend_detail}</li>
                <li><b>Planning recommendation:</b> Align safety stock levels with peak demand forecasts, and adjust warehouse staffing to support the projected trend.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Insights unavailable.")

# ==========================================
# PAGE 5: ARIMA FORECAST (MEMBER 3 SHOWCASE)
# ==========================================
elif selected_page == "🤖 ARIMA Forecast":
    st.markdown("""
    <div style="margin-bottom: 25px;">
        <h1 style="margin: 0; font-size: 32px; font-weight: 800; color: #ffffff;">🤖 ARIMA Advanced Forecast</h1>
        <div class="subtitle">Advanced time-series forecasting using the ARIMA model.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate evaluation metrics dynamically
    arima_actuals = advanced_forecast_df["Actual"].values
    arima_predictions = advanced_forecast_df["ARIMA_Prediction"].values
    
    arima_rmse = np.sqrt(np.mean((arima_actuals - arima_predictions) ** 2))
    arima_mape = calculate_mape(arima_actuals, arima_predictions)
    
    mean_actual = arima_actuals.mean()
    mean_pred = arima_predictions.mean()
    
    # Purple/blue themed KPI cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("ARIMA RMSE", f"{arima_rmse:,.2f}", "Root Mean Squared Error", "📉", "#8b5cf6") # Purple
    with col2:
        render_kpi_card("ARIMA MAPE", f"{arima_mape:.2f}%", "Mean Absolute Pct Error", "📊", "#a855f7") # Purple Accent
    with col3:
        render_kpi_card("Average Actual", f"{mean_actual:,.1f}", "Validation period actual mean", "📦", "#3b82f6") # Blue
    with col4:
        render_kpi_card("Average Prediction", f"{mean_pred:,.1f}", "Model prediction mean", "🔮", "#6366f1") # Blue-purple
        
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    # Main Chart: Actual vs ARIMA Prediction
    st.markdown("### 📈 Actual vs ARIMA Prediction")
    if not advanced_forecast_df.empty:
        fig_arima = go.Figure()
        
        # Actual Demand
        fig_arima.add_trace(go.Scatter(
            x=advanced_forecast_df["Date"],
            y=advanced_forecast_df["Actual"],
            mode="lines",
            name="Actual Demand",
            line=dict(color="#2563eb", width=2),
            hovertemplate="Date: %{x|%d %b %Y}<br>Actual Sales: %{y:,.0f}<extra></extra>"
        ))
        
        # ARIMA prediction
        fig_arima.add_trace(go.Scatter(
            x=advanced_forecast_df["Date"],
            y=advanced_forecast_df["ARIMA_Prediction"],
            mode="lines",
            name="ARIMA Prediction",
            line=dict(color="#8b5cf6", width=2, dash="dash"),
            hovertemplate="Date: %{x|%d %b %Y}<br>ARIMA Prediction: %{y:,.0f}<extra></extra>"
        ))
        
        apply_plotly_theme(fig_arima, "Model Fit: Actual Sales vs ARIMA Predictions over Time", "Date", "Demand (Units)")
        st.plotly_chart(fig_arima, use_container_width=True)
    else:
        st.info("ARIMA predictions dataset is empty.")
        
    # Section: ARIMA Model Workflow
    st.markdown("### ARIMA Model Workflow")
    st.markdown("""
    <div style="background-color: #ffffff; border-radius: 12px; padding: 25px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0,0,0,0.02); margin-bottom: 20px;">
        <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 10px;">
            <div style="background-color: #f1f5f9; padding: 10px 15px; border-radius: 8px; font-weight: 600; color: #3b82f6; font-size: 13px;">Historical Demand</div>
            <div style="color: #64748b; font-weight: bold;">➔</div>
            <div style="background-color: #f1f5f9; padding: 10px 15px; border-radius: 8px; font-weight: 600; color: #3b82f6; font-size: 13px;">Time-Series Processing</div>
            <div style="color: #64748b; font-weight: bold;">➔</div>
            <div style="background-color: #f1f5f9; padding: 10px 15px; border-radius: 8px; font-weight: 600; color: #8b5cf6; font-size: 13px;">ARIMA Model</div>
            <div style="color: #64748b; font-weight: bold;">➔</div>
            <div style="background-color: #f1f5f9; padding: 10px 15px; border-radius: 8px; font-weight: 600; color: #8b5cf6; font-size: 13px;">Model Prediction</div>
            <div style="color: #64748b; font-weight: bold;">➔</div>
            <div style="background-color: #f1f5f9; padding: 10px 15px; border-radius: 8px; font-weight: 600; color: #10b981; font-size: 13px;">Forecast Evaluation</div>
            <div style="color: #64748b; font-weight: bold;">➔</div>
            <div style="background-color: #f1f5f9; padding: 10px 15px; border-radius: 8px; font-weight: 600; color: #10b981; font-size: 13px;">Future Demand Planning</div>
        </div>
        <p style="margin-top: 15px; margin-bottom: 0; color: #475569; font-size: 13.5px; line-height: 1.6;">
            The ARIMA model uses historical time-series patterns to generate demand predictions. Forecast performance is evaluated using RMSE and MAPE.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Section: Forecast Model Comparison
    st.markdown("### 📊 Forecast Model Comparison")
    
    # Merge historical dataset's Demand Forecast with ARIMA
    hist_agg_comp = historical_df.groupby("Date", as_index=False).agg({
        "Units Sold": "sum",
        "Demand Forecast": "sum"
    })
    
    overlap_df = pd.merge(advanced_forecast_df, hist_agg_comp, on="Date", how="inner")
    
    if not overlap_df.empty:
        # Calculate comparison metrics
        base_actuals = overlap_df["Actual"].values
        base_preds = overlap_df["Demand Forecast"].values
        
        base_rmse = np.sqrt(np.mean((base_actuals - base_preds) ** 2))
        base_mape = calculate_mape(base_actuals, base_preds)
        
        # Render clean performance comparison table
        model_metrics = pd.DataFrame({
            "Model Selection": ["ARIMA Forecast Model (Advanced)", "SMA Baseline Model (Legacy)"],
            "RMSE (Lower is Better)": [f"{arima_rmse:.2f}", f"{base_rmse:.2f}"],
            "MAPE (Lower is Better)": [f"{arima_mape:.2f}%", f"{base_mape:.2f}%"],
            "Prediction Count": [len(advanced_forecast_df), len(overlap_df)]
        })
        
        st.dataframe(model_metrics, use_container_width=True)
        
        # Add visual comparison line chart
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Scatter(
            x=overlap_df["Date"],
            y=overlap_df["Actual"],
            mode="lines",
            name="Actual Demand",
            line=dict(color="#2563eb", width=2),
            hovertemplate="Date: %{x|%d %b %Y}<br>Actual: %{y:,.0f}<extra></extra>"
        ))
        
        fig_comp.add_trace(go.Scatter(
            x=overlap_df["Date"],
            y=overlap_df["ARIMA_Prediction"],
            mode="lines",
            name="ARIMA prediction (Purple)",
            line=dict(color="#8b5cf6", width=2, dash="dash"),
            hovertemplate="Date: %{x|%d %b %Y}<br>ARIMA: %{y:,.0f}<extra></extra>"
        ))
        
        fig_comp.add_trace(go.Scatter(
            x=overlap_df["Date"],
            y=overlap_df["Demand Forecast"],
            mode="lines",
            name="SMA Baseline (Grey)",
            line=dict(color="#94a3b8", width=1.5, dash="dot"),
            hovertemplate="Date: %{x|%d %b %Y}<br>Baseline: %{y:,.0f}<extra></extra>"
        ))
        
        apply_plotly_theme(fig_comp, "Comparative Projection: Actual vs ARIMA Model vs SMA Baseline Model", "Date", "Demand Units")
        st.plotly_chart(fig_comp, use_container_width=True)
    else:
        st.info("Insufficient overlapping baseline models to output comparison dashboard.")

    # Two Columns: Prediction Performance & Prediction Table
    col_perf, col_tbl = st.columns([1, 1])
    
    with col_perf:
        st.markdown("### 📊 Prediction Performance Details")
        avg_diff = np.mean(arima_predictions - arima_actuals)
        st.markdown(f"""
        <div class="insight-card">
            <h4>📋 ARIMA Evaluation Metrics</h4>
            <p>
                - <b>Validation RMSE:</b> {arima_rmse:,.2f} units<br>
                - <b>Validation MAPE:</b> {arima_mape:.2f}% error rate<br>
                - <b>Mean Bias Deviation:</b> {avg_diff:,.2f} units<br>
                - <b>Total Testing Periods:</b> {len(advanced_forecast_df)} consecutive days
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_tbl:
        st.markdown("### 📋 ARIMA Prediction Table")
        display_tbl = advanced_forecast_df.copy()
        display_tbl["Difference (Pred - Act)"] = (display_tbl["ARIMA_Prediction"] - display_tbl["Actual"]).round(2)
        display_tbl["Actual"] = display_tbl["Actual"].apply(lambda v: f"{v:,.0f}")
        display_tbl["ARIMA_Prediction"] = display_tbl["ARIMA_Prediction"].apply(lambda v: f"{v:,.2f}")
        display_tbl["Difference (Pred - Act)"] = display_tbl["Difference (Pred - Act)"].apply(lambda v: f"{v:+,.2f}")
        st.dataframe(display_tbl[["Date", "Actual", "ARIMA_Prediction", "Difference (Pred - Act)"]].head(100), use_container_width=True)
        
    # ARIMA Business Insights Section
    st.markdown("### 💡 ARIMA Business Insights")
    max_diff_idx = np.argmax(np.abs(arima_predictions - arima_actuals))
    max_diff_row = advanced_forecast_df.iloc[max_diff_idx]
    
    st.markdown(f"""
    <div class="insight-card" style="border-top: 4px solid #8b5cf6;">
        <h4 style="color: #8b5cf6 !important; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; margin-bottom: 12px;">💡 ARIMA Modeling Analytics Insights</h4>
        <ul style="color: #475569; font-size: 14.5px; line-height: 1.8; padding-left: 20px; margin-bottom: 0;">
            <li><b>Model Fit:</b> The ARIMA model predicts demand with an average percentage error of <b>{arima_mape:.2f}%</b> and standard deviation of residuals (RMSE) of <b>{arima_rmse:,.2f} units</b>.</li>
            <li><b>Peak Variance:</b> The largest forecast discrepancy occurred on <b>{max_diff_row['Date'].strftime('%d %b %Y')}</b>, where predicted demand deviated from actuals by <b>{abs(max_diff_row['ARIMA_Prediction'] - max_diff_row['Actual']):,.0f} units</b>.</li>
            <li><b>Model recommendation:</b> While the baseline ARIMA model performs very well during standard periods, integrating exogenous promotion markers (ARIMAX) is recommended to handle sudden demand shocks.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
