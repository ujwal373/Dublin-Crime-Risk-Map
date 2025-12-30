"""
Dublin Crime Risk Visualization - Streamlit App
"""
import streamlit as st
import pandas as pd
import os
from streamlit_folium import st_folium

from src.data_loader import (
    load_crime_data,
    get_available_quarters,
    get_available_regions,
    get_available_offences,
    filter_data
)
from src.scoring import (
    calculate_risk_scores,
    get_top_risky_regions,
    get_top_offences
)
from src.zones import ZoneConfig, classify_zones, get_zone_statistics
from src.viz_map import create_risk_map, create_heatmap
from src.charts import (
    create_trend_chart,
    create_top_offences_chart,
    create_region_risk_chart,
    create_offence_category_pie,
    create_quarterly_heatmap
)
from src.stations_optional import (
    load_stations_data,
    add_stations_to_map,
    add_station_clusters_to_map
)

# Page config
st.set_page_config(
    page_title="Ireland Crime Risk Visualization",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("🚨 Ireland Crime Risk Visualization")
st.markdown("Interactive dashboard for analyzing crime risk across Irish Garda regions")

# Sidebar
st.sidebar.header("Configuration")

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.df = None
    st.session_state.stations_df = None

# Load data automatically from local file
if not st.session_state.data_loaded:
    crime_data_path = "crimedata.csv"

    if os.path.exists(crime_data_path):
        try:
            with st.spinner("Loading crime data..."):
                df = load_crime_data(crime_data_path)
                st.session_state.df = df
                st.session_state.data_loaded = True

                # Get basic stats
                regions = df['Garda Region'].nunique()
                quarters = df['Quarter'].nunique()
                total_records = len(df)

            st.sidebar.success(f"✅ Data loaded successfully")
            st.sidebar.info(f"📊 {total_records:,} records\n\n🗺️ {regions} regions\n\n📅 {quarters} quarters")

        except Exception as e:
            st.error(f"❌ Error loading crime data: {e}")
            st.info("Please ensure 'crimedata.csv' exists in the project root directory")
            st.stop()
    else:
        st.error("❌ Crime data file not found!")
        st.info("""
        Please ensure 'crimedata.csv' exists in the project root directory.

        The file should contain columns:
        - Statistic Label
        - Quarter
        - Garda Region
        - Type of Offence
        - UNIT
        - VALUE
        """)
        st.stop()

# Optional: Load stations data if available
stations_path = "data/sample_stations.csv"
if os.path.exists(stations_path) and st.session_state.stations_df is None:
    try:
        stations_df = load_stations_data(stations_path)
        if stations_df is not None:
            st.session_state.stations_df = stations_df
    except Exception as e:
        pass  # Stations are optional

# Main app - data is loaded
df = st.session_state.df

# Filters in sidebar
st.sidebar.subheader("🔍 Filters")

# Quarter range selector
available_quarters = get_available_quarters(df)
if len(available_quarters) > 1:
    quarter_range = st.sidebar.select_slider(
        "Select Quarter Range",
        options=available_quarters,
        value=(available_quarters[0], available_quarters[-1])
    )
    selected_quarters = [q for q in available_quarters
                        if quarter_range[0] <= q <= quarter_range[1]]
else:
    selected_quarters = available_quarters
    st.sidebar.info(f"Single quarter available: {available_quarters[0]}")

# Region filter
available_regions = get_available_regions(df)
selected_regions = st.sidebar.multiselect(
    "Garda Regions",
    options=available_regions,
    default=available_regions,
    help="Select regions to include in analysis"
)

# Offence type filter
available_offences = get_available_offences(df)
selected_offences = st.sidebar.multiselect(
    "Offence Types",
    options=available_offences,
    default=available_offences,
    help="Select offence types to include"
)

# Zone configuration
st.sidebar.subheader("⚙️ Zone Thresholds")
st.sidebar.markdown("Adjust percentiles for risk zone classification:")

danger_percentile = st.sidebar.slider(
    "Danger Zone (top %)",
    min_value=70,
    max_value=95,
    value=80,
    step=5,
    help="Top percentile classified as Danger zone"
)

warning_percentile = st.sidebar.slider(
    "Warning Zone (middle %)",
    min_value=30,
    max_value=70,
    value=50,
    step=5,
    help="Middle percentile classified as Warning zone"
)

zone_config = ZoneConfig(
    danger_percentile=danger_percentile,
    warning_percentile=warning_percentile
)

# Map visualization options
st.sidebar.subheader("🗺️ Map Options")
map_type = st.sidebar.radio(
    "Map Type",
    options=["Risk Zones", "Heatmap"],
    help="Choose visualization style"
)

show_stations = st.sidebar.checkbox(
    "Show Stations (if available)",
    value=False,
    disabled=st.session_state.stations_df is None
)

show_clusters = st.sidebar.checkbox(
    "Show Station Clusters",
    value=False,
    disabled=st.session_state.stations_df is None or not show_stations
)

# Filter data
filtered_df = filter_data(
    df,
    quarters=selected_quarters,
    regions=selected_regions,
    offences=selected_offences
)

if len(filtered_df) == 0:
    st.warning("⚠️ No data matches the selected filters. Please adjust your selection.")
    st.stop()

# Calculate risk scores and zones
risk_df = calculate_risk_scores(filtered_df)
zones_df = classify_zones(risk_df, zone_config)

# Main layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ Crime Risk Map")

    # Create map
    if map_type == "Risk Zones":
        crime_map = create_risk_map(zones_df)
    else:
        crime_map = create_heatmap(zones_df)

    # Add stations if enabled
    if show_stations and st.session_state.stations_df is not None:
        if show_clusters:
            crime_map = add_station_clusters_to_map(crime_map, st.session_state.stations_df)
        else:
            crime_map = add_stations_to_map(crime_map, st.session_state.stations_df, zones_df)

    # Display map
    st_folium(crime_map, width=None, height=600)

with col2:
    st.subheader("📊 Zone Statistics")

    # Zone distribution
    zone_stats = get_zone_statistics(zones_df)

    for zone in ['Danger', 'Warning', 'Safe']:
        if zone in zone_stats['counts']:
            count = zone_stats['counts'][zone]
            pct = zone_stats['percentages'][zone]

            color_map = {
                'Danger': '🔴',
                'Warning': '🟡',
                'Safe': '🟢'
            }

            st.metric(
                f"{color_map[zone]} {zone} Zones",
                f"{count} regions",
                f"{pct:.1f}%"
            )

    st.markdown("---")

    # Total stats
    st.metric("Total Regions", zone_stats['total_regions'])
    st.metric("Total Incidents", int(filtered_df['VALUE'].sum()))
    st.metric("Selected Quarters", len(selected_quarters))

# Student Alerts Panel
st.subheader("🎓 Student Alerts")

alert_col1, alert_col2 = st.columns(2)

with alert_col1:
    st.markdown("### Top 10 Risky Regions")
    top_risky = get_top_risky_regions(zones_df, top_n=10)

    for idx, row in top_risky.iterrows():
        zone_emoji = {'Danger': '🔴', 'Warning': '🟡', 'Safe': '🟢'}[row['zone']]
        st.markdown(
            f"{zone_emoji} **{row['Garda Region']}**  \n"
            f"Risk Score: {row['risk_score']:.1f} | Incidents: {int(row['total_incidents'])}"
        )

with alert_col2:
    st.markdown("### Top 10 Offence Types")
    top_offences_list = get_top_offences(filtered_df, top_n=10)

    for idx, row in top_offences_list.iterrows():
        offence = row['Type of Offence']
        incidents = int(row['total_incidents'])
        # Truncate long offence names
        if len(offence) > 40:
            offence = offence[:37] + "..."
        st.markdown(f"**{offence}**  \nIncidents: {incidents}")

# Charts
st.subheader("📈 Trends and Analysis")

chart_tab1, chart_tab2, chart_tab3, chart_tab4 = st.tabs([
    "Incident Trends",
    "Top Offences",
    "Risk by Region",
    "Heatmap"
])

with chart_tab1:
    trend_fig = create_trend_chart(filtered_df)
    st.plotly_chart(trend_fig, use_container_width=True)

with chart_tab2:
    offences_fig = create_top_offences_chart(top_offences_list)
    st.plotly_chart(offences_fig, use_container_width=True)

    # Pie chart
    pie_fig = create_offence_category_pie(filtered_df)
    st.plotly_chart(pie_fig, use_container_width=True)

with chart_tab3:
    risk_fig = create_region_risk_chart(zones_df)
    st.plotly_chart(risk_fig, use_container_width=True)

with chart_tab4:
    heatmap_fig = create_quarterly_heatmap(filtered_df)
    st.plotly_chart(heatmap_fig, use_container_width=True)

# Data table
with st.expander("📋 View Detailed Data"):
    st.dataframe(
        zones_df[['Garda Region', 'risk_score', 'total_incidents', 'zone']],
        use_container_width=True
    )

# Footer
st.markdown("---")
st.markdown(
    "**Dublin Crime Risk Visualization** | "
    "Data-driven insights for student safety and awareness"
)
